#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Soubor:  pybotslib.py
# Datum:   27.09.2015 23:21
# Autor:   Marek Nožka, nozka <@t> spseol <d.t> cz
# Licence: GNU/GPL
# Úloha:   Malá knihovna pro komunikaci s pybot-serverem
############################################################################
import json
import http.client
from pprint import pprint
from urllib.parse import urlencode


class MyBot:

    def __init__(self, host='localhost', port='44822'):
        self.host = host
        self.port = port
        self.conn = http.client.HTTPConnection(host, port)
        self.conn.request("GET", "/")
        resp = self.conn.getresponse()
        if resp.status == 200:
            data = resp.read().decode('UTF-8')
            data = json.loads(data)
            self.botid = data['id']
            # print(data['id'])
        else:
            print(resp.status, resp.reason)
            print()
            pprint(resp.getheaders())
            print()
            print(resp.read().decode('UTF-8'))
            raise Exception("Hru se nepodařilo založit")

    def getmap(self):
        self.conn.request("GET", "/game/{}".format(self.botid))
        resp = self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))['map']

    def get(self, path, **param):
        enc_param = urlencode(param)
        self.conn.request('GET', '{}?{}'.format(path, enc_param))
        resp = self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))

    def post(self, path, **param):
        enc_param = urlencode(param)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain, application/json"}
        self.conn.request("POST", path, enc_param, headers)
        resp = self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    karel = MyBot('hroch.spseol.cz')
    print(karel.getmap())
    print(karel.get('/game/{}'.format(karel.botid)))
    print(karel.get('/game/{}'.format(karel.botid), a=5, b='ahoj'))
