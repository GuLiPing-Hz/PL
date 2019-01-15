import redis
import pymysql

def cleanUsers(start=None,end=None):

	if not start or not end:
		connection = pymysql.connect(host='121.196.203.52',
	                             user="root",
	                             password="gate%buyu_test",
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

	r = redis.Redis(host='121.196.203.52', port=6379, db=0,password="C9BE6E8D-F2CF-4154-BD34-922844BEAC11")
	# print(dir(r))
	for i in range(start,end):
		print("del usr_"+str(i),r.delete("usr_"+str(i)))
		r.delete("usrStat_"+str(i))

def cleanUsrByUids(uids):
	r = redis.Redis(host='121.196.203.52', port=6379, db=0,password="C9BE6E8D-F2CF-4154-BD34-922844BEAC11")
	# print(dir(r))
	for i in range(len(uids)):
		uid = uids[i]
		print("del usr_"+str(uid),r.delete("usr_"+str(uid)))
		r.delete("usrStat_"+str(uid))

if __name__ == '__main__':
	print("清理redis 测试服缓存...")
	cleanUsers() #清除所有人的redis缓存，慎用
	# cleanUsrByUids([165616]) #清除指定uid

