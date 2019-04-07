import redis
import pymysql
# import redaline

def resetUsrCard(uid):
	pass
	
	
def cleanUsers(pwd,pwd2,start=None,end=None):
	if not start or not end:
		connection = pymysql.connect(host='121.196.203.52',
	                             user="root",
	                             password=pwd,
	                             db="Buyu",
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
		# print(connection)

		#use cursor()
		cursor = connection.cursor()

		if not start:
			cursor.execute("select min(uid) as uid from user;")
			vMin = cursor.fetchone()
			start = vMin["uid"]

		if not end:
			cursor.execute("select max(uid) as uid from user;")
			vMax = cursor.fetchone()
			end = vMax["uid"]

	r = redis.Redis(host='121.196.203.52', port=6379, db=0,password=pwd2)
	# print(dir(r))
	for i in range(start,end):
		print("del usr_"+str(i),r.delete("usr_"+str(i)))
		r.delete("usrStat_"+str(i))

def cleanUsrByUids(uids,pwd,host=None):
	host = host or '121.196.203.52'
	r = redis.Redis(host=host, port=6379, db=0,password=pwd)
	# print(dir(r))

	for i in range(len(uids)):
		uid = uids[i]
		print("del usr_"+str(uid),r.delete("usr_"+str(uid)))

def cleanUsrAndStat(pwd,pattern="",host=None):
	host = host or '121.196.203.52'
	r = redis.Redis(host=host, port=6379, db=0,password=pwd)
	# print(dir(r))

	keys = r.keys()
	for i in range(len(keys)):
		theKey = (keys[i]).decode("utf-8") #byte -> str
		print(theKey)
		if pattern == "":
			print("del "+theKey,r.delete(theKey))
		elif theKey.startswith(pattern):
			print("del "+theKey,r.delete(theKey))


def testRedis():
	r = redis.Redis(host='121.196.203.52', port=6379, db=0,password=redisPwd)
	token = "bfb38d68b426b5cb96cd5d8f44aed117"
	print(r.exists(token))
	print(r.get(token))
	print(r.get("token_188787"))
	print(r.keys())


if __name__ == '__main__':
	print("清理redis 测试服缓存...")
	#启动redis 
	#./src/redis-server ../redis.conf

	mySqlPwd1 = ""
	mySqlPwd2 = ""
	redisPwd = ""
	with open("mysqlpwd.txt","r") as f:
		mySqlPwd1 = f.readline()[:-1]
		mySqlPwd2 = f.readline()[:-1]
		redisPwd = f.readline()
	print(mySqlPwd1,mySqlPwd2,redisPwd)


	# cleanUsers(mySqlPwd1,redisPwd) #清除所有人的redis缓存，慎用 -这个方法最low，从数据获取到uid最大的
	# cleanUsrByUids([100090],redisPwd,"127.0.0.1") #清除指定uid

	# cleanUsrByUids([167362],redisPwd) #清除指定uid

	# cleanUsrAndStat(redisPwd,"wx_") #清除微信登录授权信息
	# cleanUsrAndStat(redisPwd,"usr_") #清除用户缓存信息
	# cleanUsrAndStat(redisPwd,"usr_today_") #清除用户当日缓存信息
	cleanUsrAndStat(redisPwd)#清除所有人的redis缓存，慎用

	
	# testRedis()

