# pip install redis
import redis
import pymysql
import re
# import readline


def resetUsrCard(uid):
    pass


def cleanUsers(pwd, pwd2, start=None, end=None):
    if not start or not end:
        connection = pymysql.connect(host='127.0.0.1',
                                     user="root",
                                     password=pwd,
                                     db="Buyu",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        # print(connection)

        # use cursor()
        cursor = connection.cursor()

        if not start:
            cursor.execute("select min(uid) as uid from user;")
            vMin = cursor.fetchone()
            start = vMin["uid"]

        if not end:
            cursor.execute("select max(uid) as uid from user;")
            vMax = cursor.fetchone()
            end = vMax["uid"]

    r = redis.Redis(host='127.0.0.1', port=6379, db=0, password=pwd2)
    # print(dir(r))
    for i in range(start, end):
        print("del usr_"+str(i), r.delete("usr_"+str(i)))
        r.delete("usrStat_"+str(i))


def cleanUsrByUids(uids, pwd, host=None):
    host = host or '127.0.0.1'
    r = redis.Redis(host=host, port=6379, db=0, password=pwd)
    # print(dir(r))

    for i in range(len(uids)):
        uid = uids[i]
        print("del usr_"+str(uid), r.delete("usr_"+str(uid)))


def cleanUsrAndStat(pwd, pattern=None, host=None,):
    host = host or '127.0.0.1'
    r = redis.Redis(host=host, port=6379, db=0, password=pwd)
    # print(dir(r))

    keys = r.keys()
    for i in range(len(keys)):
        theKey = (keys[i]).decode("utf-8")  # byte -> str
        print("key=", theKey)
        if not pattern:
            print("del "+theKey, r.delete(theKey))
        elif pattern.match(theKey):
            print("del "+theKey, r.delete(theKey))


def testRedis():
    r = redis.Redis(host='121.196.203.52', port=6379, db=0, password=redisPwd)
    token = "bfb38d68b426b5cb96cd5d8f44aed117"
    print(r.exists(token))
    print(r.get(token))
    print(r.get("token_188787"))
    print(r.keys())


if __name__ == '__main__':
    print("清理redis 测试服缓存...")
    # 启动redis
    # ./src/redis-server ../redis.conf

    mySqlPwd1 = ""
    mySqlPwd2 = ""
    redisPwd = ""
    with open("mysqlpwd.txt", "r") as f:
        mySqlPwd1 = f.readline()[:-1]
        mySqlPwd2 = f.readline()[:-1]
        redisPwd = f.readline()
    print(mySqlPwd1, mySqlPwd2, redisPwd)

    # testRedis()

    # cleanUsers(mySqlPwd1,redisPwd) #清除所有人的redis缓存，慎用 -这个方法最low，从数据获取到uid最大的
    # cleanUsrByUids([100090],redisPwd,"127.0.0.1") #清除指定uid

    # cleanUsrAndStat(redisPwd,"wx_") #清除微信登录授权信息
    # cleanUsrAndStat(redisPwd,"usr_") #清除用户缓存信息
    # cleanUsrAndStat(redisPwd,"usr_today_") #清除用户当日缓存信息

    # cleanUsrAndStat(redisPwd)#清除所有的redis缓存，慎用

    # *匹配0次多次 +匹配一次多次 ?匹配0次1次(非贪婪)
    # \d 匹配所有数字 \D匹配任意非数字 ^匹配开头 $匹配末尾 \w匹配字母数字下划线 \W	匹配非字母数字及下划线
    pattern = None  # 这样会清理redis中所有的缓存信息
    # 下面两个很少会用
    # pattern = re.compile("^token_\\d+")#只匹配Token信息 ->建议还是用r比较方便，不然要写很多的\转义符
    # pattern = re.compile(r"^WX_\d+")#只匹配WX认证信息 ->建议还是用r比较方便，不然要写很多的\转义符

    # pattern = re.compile(r"^usr_checkin_\d+")#只匹配用户签到信息
    # pattern = re.compile(r"^usr_checkin7_\d+")#只匹配用户7日签到信息
    # pattern = re.compile(r"^usr_\d+")#只匹配用户信息
    # pattern = re.compile(r"^usr_today_\d+")#只匹配用户今日信息
    # pattern = re.compile(r"^usr_today_m_\d+")#只匹配用户今日更多信息

    # #\s 匹配所有空白字符=[\t\n\r\f]， \S 匹配所有非空白字符
    # pattern = re.compile(r"^usr_today_\S+")#匹配用户的所有今日信息，
    # pattern = re.compile(r"^usr_\S+")#匹配用户的所有信息，，在线列表的redis名字后面要换一下。。

    print("pattern=", pattern)
    # if pattern:
    # 	print("match=",pattern.match("usr_checkin7_165272"))

    host = "121.196.203.52"
    # host = "192.168.100.2"
    cleanUsrAndStat(redisPwd, pattern, host)  # 清除所有的redis缓存，慎用
