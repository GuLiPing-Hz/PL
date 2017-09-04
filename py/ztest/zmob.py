#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python 2.7
#MOB 短信请求byhttp


import urllib,urllib2
import json;

class MobSMS:
    def __init__(self, appkey):
        self.appkey = appkey
        self.url = 'https://webapi.sms.mob.com/sms/sendmsg'

    def verify_sms_code(self, zone, phone, debug=False):
        if debug:
            return 200

        data = {'appkey': self.appkey, 'zone': zone, 'phone': phone}
        data = urllib.urlencode(data)
        req = urllib2.Request(self.url, data)
        o = urllib2.urlopen(req)
        if o.getcode() == 200:
		j = json.loads(o.read())
		    return j.get("status")
        return 500

if __name__ == '__main__':
    mobsms = MobSMS('1eb63d197f5c7')
    #print mobsms.verify_sms_code(86, 15000003329)
    