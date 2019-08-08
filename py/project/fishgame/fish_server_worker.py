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

# HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
HEADERS = {"Content-type": "application/json", "Accept": "text/plain"}

# crontab 中执行的文件路径必须是全路径，否则会有问题
LOG_FILE = "/opt/py/1.txt"
PWD_FILE = "/opt/py/mysqlpwd.txt"


# 启动钉钉通知消息
def ding_text(token, content, numbers, is_all):
    """
    token：Token令牌
    content：通知内容
    numbers：通知列表
    is_all：是否全员通知
    """
    # https://oapi.dingtalk.com/robot/send?access_token=75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494

    # print("ding_text")
    conn = http.client.HTTPSConnection("oapi.dingtalk.com")
    # print(conn)

    tempHead = dict(HEADERS)
    # print("tempHead = ",tempHead);

    params_at = {"atMobiles": numbers, "isAtAll": is_all}
    # print(params_at)

    # params_content = {"content": content}
    # print(params_content)
    # dictParams = {'msgtype': 'text', "text": params_content, "at": params_at}
    whoToAt = ""
    for i in range(len(numbers)):
        whoToAt += "@"+str(numbers[i])

    params_content = {"title": "警告", "text": content+"\n"+whoToAt}
    print(params_content)
    dictParams = {'msgtype': 'markdown',
                  "markdown": params_content, "at": params_at}
    # print(dictParams)

    json_params = json.dumps(dictParams)
    # print(json_params)

    # params =  urllib.parse.urlencode(dictParams)
    # print(params)

    try:
        conn.request("POST", "/robot/send?access_token=" +
                     token, json_params, tempHead)

        response = conn.getresponse()
        data = response.read()

        # print(type(data))
        print("ding_text", response.status, response.reason,
              data.decode(), sep=' ; ')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass


def dint_text_me(text):
    numbers = ["15088603329", "18758032593"]
    ding_text("75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494",
              text, numbers, False)


def getProcByCmdline(name):
    # attrs = ['pid', 'memory_percent', 'name', 'cpu_times', 'create_time','memory_info']
    procRet = None
    attrs = ['pid', 'memory_percent', 'name',
             'cpu_times', 'memory_info', 'cmdline']
    for proc in psutil.process_iter(attrs=attrs):
        # print(proc.info)
        # print(proc)
        try:
            cmdline = proc.cmdline()
            # print(cmdline)
            if cmdline and len(cmdline) > 0 and cmdline[0] == name:
                procRet = proc
                # procRet = psutil.Process(proc.pid)
                # print(procRet == proc)
                break
        except psutil.AccessDenied as e:
            print(e)
            pass
    return procRet


def getProcByName(name):
    # attrs = ['pid', 'memory_percent', 'name', 'cpu_times', 'create_time','memory_info']
    procRet = None
    attrs = ['pid', 'memory_percent', 'name',
             'cpu_times', 'memory_info', 'cmdline']
    for proc in psutil.process_iter(attrs=attrs):
        # print(proc.info)
        if proc.name() == name:
            procRet = proc
            # procRet = psutil.Process(proc.pid)
            # print(procRet == proc)
            break
        # break
    return procRet


def getMbFromByte(bytes):
    gb = bytes/1024/1024/1024
    mb = bytes/1024/1024
    if gb > 1:
        return str(round(gb, 2))+"GB"
    else:
        return str(round(mb, 2))+"MB"


def restart(cmd):
    # os.system(cmd)#会将标准输出到这里
    # subprocess.call(cmd)#不会将标准输出到这里
    pos = cmd.rfind("/")
    cwd = cmd[:pos]
    print(pos, cwd)
    if "Windows" == platform.system():
        subprocess.Popen(cmd, cwd=cwd)
    else:
        with open("/dev/null") as f:
            subprocess.Popen(cmd, stdout=f, cwd=cwd)


def tryRestart(name, cmd):
    p = multiprocessing.Process(target=restart, args=(cmd,))
    p.start()

    time.sleep(1)
    proc = getProcByCmdline(name)
    return proc


def checkProc(name, restartCmd):
    text = ""
    proc = getProcByCmdline(name)
    if not proc or not proc.is_running():
        text += "# Exe Warning\n"
        text += "The Exe="+name+" is not running!!!\n" \
            "#### try restart="+restartCmd+"\n"

        proc = tryRestart(name, restartCmd)
        text += "result = " + str((proc and proc.is_running())) + "\n"
    return text, proc


def parseNetstatTPN(path, useLocal=True):
    """
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
    """
    newPath = path+".txt"
    try:
        os.remove(newPath)
    except FileNotFoundError:
        pass
    shutil.copy(path, newPath)
    with open(newPath, "r") as f:
        # cells = []
        dicts = {}
        for line in f:
            # print(line)
            words = line.split(" ")
            # print(words)

            cell = []
            for i in range(len(words)):
                if words[i] == "" or words[i] == "\n":
                    continue
                cell.append(words[i])
            # print(cell)
            # break
            cellDict = {
                "Proto": cell[0], "Recv-Q": cell[1], "Send-Q": cell[2],
                "Local-Address": cell[3], "Foreign-Address": cell[4],
                "State": cell[5], "PID-Program-name": cell[6]
            }
            if useLocal:
                if cell[3].startswith("127.0.0.1"):
                    if cell[3] != "127.0.0.1:3306":
                        dicts[cell[3]] = cellDict
                else:
                    dicts[cell[4]] = cellDict
            else:
                dicts[cell[3]] = cellDict
            # cells.append(cell)
        # print(cells)
        return dicts


def getMySqlState(isProduction, host, user, pwd, db):
    """
            return 4个值（mysql最大连接数，历史最大连接数，线程数，当前连接的程序）
    """

    if "Windows" != platform.system():
        os.system("netstat -tpn | grep 3306 > netstat.txt")
    netstats = parseNetstatTPN("./netstat.txt", not isProduction)

    # open db connection
    # Connect to the database
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=pwd,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # print(connection)

    # use cursor()
    cursor = connection.cursor()
    # print(cursor)

    # use execute() run sql
    cursor.execute("show variables like '%max_connections%';")

    # USE fetchone()
    vMax = cursor.fetchone()  # fetchall
    print(vMax, type(vMax))

    cursor.execute("show global status like 'Max_used_connections';")
    vHistoryMax = cursor.fetchone()
    print(vHistoryMax, type(vHistoryMax))

    cursor.execute("show global status like 'Threads_connected';")
    vThreads = cursor.fetchone()
    # print(vThreads,type(vThreads))

    cursor.execute("show full processlist;")
    cCur = cursor.fetchall()
    print("cCur=", cCur)
    print("netstats=", json.dumps(netstats))
    procList = []
    for i in range(len(cCur)):
        val = cCur[i]
        host = val["Host"]
        # print(host in netstats)
        if host in netstats:
            val["Netstat"] = netstats[host]
            procList.append(val)
        elif val["Info"] != "show full processlist":
            procList.append(val)
    print("procList=", json.dumps(procList))

    # print("\n--------------------------------\n")
    # print("统计日期 ：",time.strftime('%Y-%m-%d %H:%M:%S'))
    # print("mysql最大连接数 ：",Max)
    # print("mysql历史最大连接数 ：",History_max[1])
    # print("mysql当前最大连接数 ：",Currently[1])

    connection.close()

    return (int(vMax["Value"]), int(vHistoryMax["Value"]),
            int(vThreads["Value"]), procList)

def worker(isProduction, mysql, thresholdCpu,thresholdCpuSingle, thresholdAvailableMem, path, thresholdFreeeDisk, names, restartCmds):
    """
    isProduction True表示正式服，False测试服
    thresholdMysql myslq连接数上限阈值
    thresholdCpu cpu报警上限阈值
    thresholdAvailableMem 内存可用下限阈值
    path 指定路径位置
    thresholdFreeeDisk 指定路径的磁盘可用下限阈值
    names 指定检查的进程名字列表
    restartCmds 指定对应的重启命令列表
    """
    t = type(names)
    arrayType = type([])
    print(t, t == arrayType)
    if type(names) != arrayType or type(restartCmds) != arrayType or len(names) != len(restartCmds):
        raise ValueError("need array")

    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    # print(now.ctime())
    curTime = str(date) + "." + str(now.microsecond) + "\n"
    if not isProduction:
        curTime += "## Test\n"
    print("working", curTime)
    text = curTime

    procs = []
    for i in range(len(names)):
        procText, proc = checkProc(names[i], restartCmds[i])
        # print(proc)
        # print(proc.exe())
        # print("cmdline=",proc.cmdline())
        # if "Windows" == platform.system():
        # 	print("num_handles=",proc.num_handles())
        # else:
        # 	print("num_fds=",proc.num_fds())
        # print("num_threads=",proc.num_threads())
        # print("memory_info=",proc.memory_info())
        # print("memory_percent=",proc.memory_percent())
        # print("connections=",proc.connections())

        text += procText
        if proc:
            procs.append(proc)

    if text == curTime:  # 所有程序都在正常运行,检查运行状态
        cpu = psutil.cpu_percent(interval=0.1)
        # 测试发现简单所有的cpu没有的，要检查主要的程序的cpu
        print("*"*60)
        print("cpu=", cpu, "cpucnt=", psutil.cpu_count())
        if(cpu > thresholdCpu):
            text += "# CPU TOTAL Warning\n"
            text += "#### TOTAL CPU=" + \
                str(cpu)+" is over threshold("+str(thresholdCpu)+").\n"

        # 检查单个cpu运行状况
        for i in range(len(procs)):
            exeCpu = procs[i].cpu_percent(0.1)
            print("cpu["+names[i]+"]="+str(exeCpu)+"\n")
            if exeCpu > thresholdCpuSingle:
                text += "# CPU Single Warning\n"
                text += "#### ["+names[i]+",cpu="+str(exeCpu)+">"+str(thresholdCpuSingle)+"]\n"
        # print("*"*60)
        vm = psutil.virtual_memory()
        # print("virtual_memory=",type(vm), vm)
        print("*"*60)
        print("virtual_memory=",vm.total, vm.available, vm.percent,"<",thresholdAvailableMem)  # 查看虚拟内存
        if(vm.available < thresholdAvailableMem):
            text += "# Memory Warning\n"
            text += "#### TOTAL Memory Available="+getMbFromByte(vm.available)+" is under threshold(" \
                + getMbFromByte(thresholdAvailableMem)+").\n"

            for i in range(len(procs)):
                proc = procs[i]
                # 下面用5个#，虽然字体大小不变，但是可以强制钉钉内容换行。
                text += "##### ["+names[i]+" memory_percent="+str(round(proc.memory_percent(), 2)) \
                    + "%,rss(虚拟耗用内存)="+getMbFromByte(proc.memory_info().rss)+",vms(实际物理内存)=" \
                    + getMbFromByte(proc.memory_info().vms)+"]\n"
            text += "\n"

        # print("*"*60)
        # print("disk_partitions=",psutil.disk_partitions())  # 查看硬盘分区
        print("*"*60)
        pathDiskUsage = psutil.disk_usage(path)
        print("disk_usage=",pathDiskUsage,pathDiskUsage.free,"<",thresholdFreeeDisk)  # 查看硬盘使用
        # print("*"*60)
        if(pathDiskUsage.free < thresholdFreeeDisk):
            text += "# Disk Warning\n"
            text += "#### Disk("+path+") Free="+getMbFromByte(pathDiskUsage.free) \
                + " is under threshold(" + \
                getMbFromByte(thresholdFreeeDisk)+")\n"
        # print("net_io_counters=",psutil.net_io_counters(pernic=True))  # 查看网络链接

        mysqlState = getMySqlState(isProduction, mysql[0], mysql[1], mysql[2], mysql[3])
        thresholdConnections = mysqlState[0]*mysql[4]
        curConnections = len(mysqlState[3])
        mysqlProcList = mysqlState[3]
        print("*"*60)
        print("myslq connections", thresholdConnections, curConnections)
        if thresholdConnections < curConnections:
            text += "# Mysql Connections Warning\n"
            text += "#### Connections="+str(curConnections)+" is over threshold(" \
                + str(thresholdConnections)+")\n"
            text += "#### ConnectionsInfo Max="+str(mysqlState[0]) \
                + " HistoryMax=" + \
                    str(mysqlState[1])+" Threads="+str(mysqlState[2])+"\n"

            for i in range(len(mysqlProcList)):
                proc = mysqlProcList[i]
                programName = "unknow-" + proc["User"]
                if "Netstat" in proc and proc["Netstat"]:
                    programName = proc["Netstat"]["PID-Program-name"]

                text += "##### ["+programName+",db="+str(proc["db"]) \
                    + ",Command="+proc["Command"]+",Time="+str(proc["Time"])+",State="+proc["State"] \
                    + ",Info="+str(proc["Info"])+",Host="+proc["Host"]+"]\n"

    if text != curTime:
        print(text)
        dint_text_me(text)
        pass


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

    cpuLimit = 100
    # #@注意 路径必须以 / 分隔
    if len(sys.argv) >= 2 and sys.argv[1] == "debug":  # 测试服
        names = ["/opt/tcpproxy1/tcpproxy"]
        cmds = ["/opt/tcpproxy1/start.sh"]
        mysql = ["127.0.0.1", "root", mySqlPwd2, "Buyu", 0.5]
        print("pwd=", mySqlPwd2)
    else:  # 正式服
        IsProduction = True
        names = ["/opt/fish/skynet/skynet", "/opt/auth/auth", "/opt/xqtpay/xqtpay",
                 "/opt/slot/slot"]
        cmds = ["/opt/fish/sh_start.sh", "/opt/auth/start.sh",
                "/opt/xqtpay/start.sh", "/opt/slot/start.sh"]
        mysql = ["192.168.100.2", "root", mySqlPwd1, "Buyu", 0.8]
        print("pwd=", mySqlPwd1)
        cpuLimit = 200

    print(names)
    worker(IsProduction, mysql, 90,cpuLimit, mb100, "/home", mb1000, names, cmds)

    # 单个函数测试
    # checkProc("fishjs.exe","D:/glp/Github/Fish2/frameworks/runtime-src/proj.win32/Debug.win32/fishjs.exe")
    # checkProc("skynet","/opt/fish/sh_start.sh")
    # checkMySql("127.0.0.1","glp4703","glp3329","databasetest")
    # getMySqlState("127.0.0.1","root","gate%buyu_test","Buyu")
    # parseNetstatTPN("../../test/netstat.txt")
