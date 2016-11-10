import http.client, urllib.parse
from datetime import datetime, date, time
import time as _time
import random
import hashlib

IS_TEST = False
#必须要增加这个headers，否则会提示参数错误
HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
HTTP_HEADER_TOKEN = "Dddi23*DOO#LKD3"

def get_sign(rand,time):
	array = [str(rand),str(time),HTTP_HEADER_TOKEN]
	#print("array =", array,type(array))
	array.sort() # 对array 进行排序
	#print("array =", array)

	result = ""
	for s in array :
		result += s
	return hashlib.sha1(bytes(result,encoding="utf_8")).hexdigest()

def get_md5(params):
	s = HTTP_HEADER_TOKEN

	keys = params.keys()
	keys = sorted(keys)
	for key in keys:
		s = s+str(key)+str(params[key])
	print("md5 origin =",s)
	return hashlib.md5(bytes(s,"utf_8")).hexdigest()

def add_head(params):
	utcTime = int(_time.time())
	print("utcTime = ",utcTime)
	randNum = int(random.random()*(9999-1000))+1000
	print("randNum = ",randNum)

	sign1 = get_sign(randNum,utcTime);
	print("sign1 = ",sign1)

	sign2 = get_md5(params)
	print("sign2 = ",sign2)

	head = {};
	head["04B29480233F4DEF5C875875B6BDC3B1"] = sign1
	head["34D1C35063280164066ECC517050DA0B"] = randNum
	head["07CC694B9B3FC636710FA08B6922C42B"] = utcTime
	head["8D777F385D3DFEC8815D20F7496026DC"] = sign2 # md5
	head["my-app-ver"] = "1.3.2" #app 版本号
	head["area"] = "86" #app 地区版本

	return head

#战鱼比赛报名
def check_in(conn,uid,code):
	'''
	conn：HTTPConnection连接
	uid: 用户ID
	code: 指定需要加入的牌局
	'''
	print("current uid is ",uid,"do check in!")

	tempHead = dict(HEADERS)
	print("tempHead = ",tempHead);
	
	dictParams = {'uid': uid, 'code': code, "os": 1} # 1 android
	authHead = add_head(dictParams)
	print("authHead = ",authHead);
	tempHead.update(authHead)
	print("tempHead = ",tempHead);

	params =  urllib.parse.urlencode(dictParams)
	#print(params)

	try:
		conn.request("POST", "/game/mttcheckin", params, tempHead)
	except Exception as e:
		print(str(e))
	else:
		pass
	finally:
		pass
	
	response = conn.getresponse()
	data = response.read()
	print(response.status, response.reason, data,sep=';') #指定分隔符


def check_in_number(num,code):
	#战鱼德州
	#报名参加MTT 

	'''
	请求域名的HttpConnection方法
	'''
	# h1 = http.client.HTTPConnection('www.python.org')    #指定域名
	# h2 = http.client.HTTPConnection('www.python.org:80') #指定域名，端口
	# h3 = http.client.HTTPConnection('www.python.org', 80) #指定域名，端口
	# h4 = http.client.HTTPConnection('www.python.org', 80, timeout=10) #指定域名，端口，超时时间

	url = ""
	if(IS_TEST):
		url = "120.27.162.46:8009"
	else:
		url = "api.sociapoker.com"
	conn = http.client.HTTPConnection(url)

	formalUids = [110191,110192,110195,103265,109886,102243,104859,134975,135061,110457,135569]

	if(IS_TEST):
		for uid in range(10000,10000+num):
			check_in(conn,uid,code)
	else:
		end = min(len(formalUids),num)
		for uid in range(0,end):
			check_in(conn,formalUids[uid],code)


def login():
	pass


if __name__ == '__main__':
	check_in_number(100,892621)
