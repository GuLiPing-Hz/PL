#! python3.4

#Http 模块
import http.client, urllib.parse
#日期
from datetime import datetime, date, time
#UTC time
import time as _time
#随机数
import random
#md5 sh1 加密模块
import hashlib
#json解析模块
import json

#HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
HEADERS = {"Content-type": "application/json","Accept": "text/plain"} 

#启动钉钉通知消息
def ding_text(token,content,numbers,is_all):
	"""
	token：Token令牌
	content：通知内容
	numbers：通知列表
	is_all：是否全员通知
	"""

	print("ding_text")
	conn = http.client.HTTPSConnection("oapi.dingtalk.com")
	print(conn)

	tempHead = dict(HEADERS)
	#print("tempHead = ",tempHead);
	
	params_content = {"content":content}
	print(params_content)

	params_at = {"atMobiles":numbers,"isAtAll":is_all}
	print(params_at)
	dictParams = {'msgtype': 'text', "text": params_content, "at": params_at}
	print(dictParams)

	json_params = json.dumps(dictParams)
	print(json_params)

	# params =  urllib.parse.urlencode(dictParams)
	# print(params)

	try:
		conn.request("POST", "/robot/send?access_token="
			+token, json_params, tempHead)

		response = conn.getresponse()
		data = response.read()

		#print(type(data))
		print(response.status, response.reason, data.decode(),sep=' ; ') #指定分隔符
	except Exception as e:
		print(str(e))
	else:
		pass
	finally:
		pass

if __name__ == '__main__':
	#main()
	numbers = ["13732293103"]

	"""
	Token令牌
	通知内容
	通知列表
	是否全员通知
	"""
	ding_text("f65cce87009618e5ba38b901aa2a0405f05832fca03da130ce5feea569f55709"
		,"Hello World",numbers,True)

