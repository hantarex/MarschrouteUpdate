from src.curl import Curl
from src.mysql import Mysql
from src.define import *
import threading, time
import sys

weight = 5
oneLength = round(pow((weight * 5000), 1 / 3)) * 10
threadCount = 4

threads = []
workList = []


def getInfo(index, city, left):
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

    if (result == True):
        mysql.updatePosition(index)
    # print(index, city, result)

    text = "Запись: " + str(index) + " " + str(city) + " " + str(result) + " осталось: " + str(left) + " Время: " + str(avrReq)
    # sys.stdout.write('\r' + str(text))
    # sys.stdout.flush()
    print(text)


curl = Curl()
mysql = Mysql()

[res, count] = mysql.getIndex()
i = 0
for row in res:
    index = row['inx']
    city = row['city']
    t = threading.Event()
    x = threading.Thread(target=getInfo, args=(index, city, (count - i)))
    x.start()
    while threading.active_count() > threadCount + 1:
        time.sleep(0.1)
    i += 1
