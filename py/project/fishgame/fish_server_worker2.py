#! python3.4
# @ guliping
import multiprocessing
import platform
import os
import subprocess
import datetime
import shutil
# 查看系统运行状态 pip install psutil
# https://pypi.org/project/psutil/
import psutil
# pip install pymysql
import pymysql

# Http 模块
import http.client
import urllib.parse

# UTC time
import time
# 随机数
import random
# md5 sh1 加密模块
import hashlib
# json解析模块
import json
import fish_server_worker

# HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
HEADERS = {"Content-type": "application/json", "Accept": "text/plain"}

# crontab 中执行的文件路径必须是全路径，否则会有问题
LOG_FILE = "/opt/py/1.txt"
PWD_FILE = "/opt/py/mysqlpwd.txt"


if __name__ == '__main__':
    import sys

    mb100 = 100*1024*1024
    mb1000 = 1000*1024*1024
    mb10000000 = 10000000*1024*1024
    # worker(10,mb100,"/",mb100,["fishjs.exe"],["D:/glp/Github/Fish2/frameworks/runtime-src/proj.win32/Debug.win32/fishjs.exe"])
    names = []
    cmds = []
    mysql = []

    print(sys.argv, len(sys.argv))

    IsProduction = False

    mySqlPwd1 = ""
    mySqlPwd2 = ""
    # print("Test 1")
    with open("/opt/py/mysqlpwd.txt", "r") as f:
        pass
        mySqlPwd1 = f.readline()[:-1]
        mySqlPwd2 = f.readline()[:-1]
    print("MySqlPwd=", mySqlPwd1, mySqlPwd2)

    # #@注意 路径必须以 / 分隔
    cpuLimit = 100
    if len(sys.argv) >= 2 and sys.argv[1] == "debug":  # 测试服
        names = ["/opt/tcpproxy2/tcpproxy"]
        cmds = ["/opt/tcpproxy2/start.sh"]
        mysql = ["127.0.0.1", "root", mySqlPwd2, "Buyu", 0.5]
        print("pwd=", mySqlPwd2)
    else:  # 正式服
        IsProduction = True
        # 正式服，目前auth用的是auth2，slot用的slot2
        names = ["/opt/fish2/skynet/skynet", "/opt/auth2/auth",
                 "/opt/xqtpay/xqtpay", "/opt/slot/slot"]
        cmds = ["/opt/fish2/sh_start.sh", "/opt/auth2/start.sh",
                "/opt/xqtpay/start.sh", "/opt/slot/start.sh"]
        mysql = ["192.168.100.2", "root", mySqlPwd1, "Buyu", 0.8]
        print("pwd=", mySqlPwd1)
        cpuLimit = 200
    print(names)
    fish_server_worker.worker(IsProduction, mysql, 90,cpuLimit, mb100, "/home", mb1000, names, cmds)

    # print(getProcByCmdline("/opt/tcpproxy_test/tcpproxy"))
    # 单个函数测试
    # checkProc("fishjs.exe","D:/glp/Github/Fish2/frameworks/runtime-src/proj.win32/Debug.win32/fishjs.exe")
    # checkProc("skynet","/opt/fish/sh_start.sh")
    # checkMySql("127.0.0.1","glp4703","glp3329","databasetest")
    # getMySqlState(False,"127.0.0.1","root","gate%buyu_test","Buyu")
    # parseNetstatTPN("../../test/netstat.txt")
