from json import JSONDecodeError

import phpserialize
import requests, time


class Curl:
    def request(self, url, param):
        # print(url + "?" + param['index'])
        r = requests.get(url, param)
        # print(r.json())
        try:
            json = r.json()
        except JSONDecodeError:
            print(r, r.headers,r.content)
            return False

        return [r.elapsed.microseconds / 1000000, phpserialize.dumps(r.json())]

    def request_tmp(self, url, param):
        time.sleep(5)
        return True
