from src.curl import Curl
from src.mysql import Mysql
from src.define import *
import threading

threads = []
workList = []


def getInfo():
    curl = Curl()
    mysql = Mysql()

    res = mysql.getIndex()

    for row in res:
        index = row['inx']
        city = row['city']
        if index not in workList:
            workList.append(index)
            print(index, workList)

            result = curl.request(url + '/' + apiKey + '/' + pages['delivery'], {
                "index": str(index),
                'weight': 499,
                'lenght': 100
            })

            # [req, serialize] = curl.request(url + '/' + apiKey + '/' + pages['delivery'], {
            #     "index": str(index),
            #     'weight': 499,
            #     'lenght': 100
            # })
            #
            # [req1, serialize_weight] = curl.request(url + '/' + apiKey + '/' + pages['delivery'], {
            #     "index": str(index),
            #     'weight': weight * 1000,
            #     'lenght': oneLength
            # })
            # result = mysql.setData(index, data={
            #     'data': serialize,
            #     'data_weight': serialize_weight,
            #     'sec': (req + req1) / 2,
            # })

            if (result == True):
                mysql.updatePosition(index)

            print(index, result)
            workList.remove(index)


for i in range(0, threadCount):
    threading.Event()
    x = threading.Thread(target=getInfo)
    threads.append(x)
    x.start()
