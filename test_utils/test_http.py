#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests


if __name__ == '__main__':

    '''
    requests 发送消息的 content-type，不仅可以通过 header 的方式设置，还可以直接通过 传递参数的类型
    '''

    res_json = requests.post('http://localhost:5000/api/json_form/1234', json={"mytext": u"三角_json_from"})
    if res_json.ok:
        print res_json.json()
        print res_json.headers

    res_urlencoded = requests.post('http://localhost:5000/api/urlencoded_form/1234', data={"mytext": u"三角_urlencoded_form"})
    if res_urlencoded.ok:
        print res_urlencoded.json()
        print res_urlencoded.headers

    res_get_urlencode = requests.get('http://localhost:5000/api/urlencoded_get/1234', params={"mytext": u"三角_urlencoded_form"})
    if res_get_urlencode.ok:
        print res_get_urlencode.json()
        print res_get_urlencode.headers