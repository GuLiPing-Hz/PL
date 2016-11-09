import http.client, urllib.parse


#战鱼德州
#报名参加MTT 

#必须要增加这个headers，否则会提示参数错误
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 


'''
请求域名的HttpConnection方法
'''
# h1 = http.client.HTTPConnection('www.python.org')    #指定域名
# h2 = http.client.HTTPConnection('www.python.org:80') #指定域名，端口
# h3 = http.client.HTTPConnection('www.python.org', 80) #指定域名，端口
# h4 = http.client.HTTPConnection('www.python.org', 80, timeout=10) #指定域名，端口，超时时间

conn = http.client.HTTPConnection("120.27.162.46:8009")


for uid in range(10000,12000):
	print("current uid is ",uid,"do check in!")
	params = urllib.parse.urlencode({'uid': uid, 'code': 739569})
	#print(params)
	conn.request("POST", "/game/mttcheckin", params,headers)
	response = conn.getresponse()
	data = response.read()
	print(response.status, response.reason, data,sep=';') #指定分隔符
 
