from src.curl import Curl
from src.mysql import Mysql
from src.define import *
import threading, time
from termcolor import colored
import sys

weight = 5
oneLength = round(pow((weight * 5000), 1 / 3)) * 10
threadCount = 3

threads = []
workList = []


def getInfo(index, city, left):
    # print("Старт: ", index)
    start_time = time.time()
    [req, serialize] = curl.request(url + '/' + apiKey + '/' + pages['delivery'], {
        "index": str(index),
        'weight': 499,
        'lenght': 100
    })

    [req1, serialize_weight] = curl.request(url + '/' + apiKey + '/' + pages['delivery'], {
        "index": str(index),
        'weight': weight * 1000,
        'lenght': oneLength
    })

    avrReq = (req + req1) / 2
    result = mysql.setData(index, data={
        'data': serialize,
        'data_weight': serialize_weight,
        'sec': avrReq,
    })

    if result:
        mysql.updatePosition(index)
    else:
        print(index, " - False")
    # print(index, city, result)
    end_time = time.time()

    if result:
        resultPrint = colored('True', 'green')
    else:
        resultPrint = colored('False', 'red')

    text = str(time.ctime()) + ": Запись: " + str(index) + " " + str(city) + " " + resultPrint + " осталось: " + str(left) + " Время запроса: " + str(avrReq) + " Время функции: " + str(end_time - start_time)
    # sys.stdout.write('\r' + str(text))
    # sys.stdout.flush()
    print(text)
    # print("Финиш: ", index)


curl = Curl()
mysql = Mysql()

[res, count] = mysql.getIndex()
i = 0
for row in res:
    index = row['inx']
    city = row['city']
    t = threading.Event()
    # print("Вход: ",index)
    x = threading.Thread(target=getInfo, args=(index, city, (count - i)))
    x.start()
    while threading.active_count() > threadCount + 1:
        time.sleep(0.1)
    i += 1
