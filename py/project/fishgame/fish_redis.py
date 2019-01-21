import redis
import pymysql

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

def cleanUsrByUids(uids,pwd):
	r = redis.Redis(host='121.196.203.52', port=6379, db=0,password=pwd)
	# print(dir(r))
	for i in range(len(uids)):
		uid = uids[i]
		print("del usr_"+str(uid),r.delete("usr_"+str(uid)))
		r.delete("usrStat_"+str(uid))

if __name__ == '__main__':
	print("清理redis 测试服缓存...")

	mySqlPwd1 = ""
	mySqlPwd2 = ""
	redisPwd = ""
	with open("mysqlpwd.txt","r") as f:
		mySqlPwd1 = f.readline()[:-1]
		mySqlPwd2 = f.readline()[:-1]
		redisPwd = f.readline()
	print(mySqlPwd1,mySqlPwd2,redisPwd)

	# cleanUsers(mySqlPwd1,redisPwd) #清除所有人的redis缓存，慎用
	cleanUsrByUids([165616],redisPwd) #清除指定uid

