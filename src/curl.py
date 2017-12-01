import phpserialize
import requests, time


class Curl:
    def request(self, url, param):
        # print(url + "?" + param['index'])
        r = requests.get(url, param)
        # print(r.json())
        return [r.elapsed.microseconds / 1000000, phpserialize.dumps(r.json())]

    def request_tmp(self, url, param):
        time.sleep(5)
        return True
