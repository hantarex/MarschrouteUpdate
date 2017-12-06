import pymysql.cursors
from src.define import *
from termcolor import colored

class Mysql:
    connection = None

    def __init__(self) -> None:
        super().__init__()
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          db=db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def getIndex(self):
        cursor = self.connection.cursor()
        sql = "select inx,city from index_city where chk=0 order by city"
        cursor.execute(sql)
        result = cursor.fetchall()
        return [result, cursor.rowcount]

    def setData(self, index, data):
        try:
            cursor = self.connection.cursor()
            sql = "insert into marschroute_delivery_utf(`index`,data,data_weight,req_time) " \
                  "values(%s, %s, %s, %s) " \
                  "on duplicate key update data=values(data), data_weight=values(data_weight), req_time=values(req_time)"
            cursor.execute(sql, (index, data['data'], data['data_weight'], data['sec']))
            self.connection.commit()
            return True
        except (AttributeError, pymysql.err.InterfaceError):
            print(colored('ReInit', 'red'))
            self.__init__()
            self.setData(index, data)

    def updatePosition(self, index):
        if len(str(index)) != 6:
            return False
        try:
            with self.connection.cursor() as cursor:
                sql = "update index_city set chk=1 where inx=%s"
                cursor.execute(sql, (index,))
            self.connection.commit()
        finally:
            return True
