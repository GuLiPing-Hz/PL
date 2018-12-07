import multiprocessing 
import platform
import os
import subprocess
import datetime
# 查看系统运行状态 pip install psutil
# https://pypi.org/project/psutil/
import psutil

#! python3.4
# @ guliping

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

#HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
HEADERS = {"Content-type": "application/json", "Accept": "text/plain"}

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
	#print("tempHead = ",tempHead);

	params_at = {"atMobiles": numbers, "isAtAll": is_all}
	# print(params_at)

	# params_content = {"content": content}
	# print(params_content)
	# dictParams = {'msgtype': 'text', "text": params_content, "at": params_at}
	whoToAt = ""
	for i in range(len(numbers)):
		whoToAt += "@"+str(numbers[i])

	params_content = {"title": "警告","text": content+"\n"+whoToAt}
	print(params_content)
	dictParams = {'msgtype': 'markdown', "markdown": params_content, "at": params_at}
	# print(dictParams)

	json_params = json.dumps(dictParams)
	# print(json_params)

	# params =  urllib.parse.urlencode(dictParams)
	# print(params)

	try:
		conn.request("POST", "/robot/send?access_token="+ token, json_params, tempHead)

		response = conn.getresponse()
		data = response.read()

		# print(type(data))
		print("ding_text",response.status, response.reason,data.decode(), sep=' ; ')  # 指定分隔符
	except Exception as e:
		print(str(e))
	else:
		pass
	finally:
		pass

def dint_text_me(text):
	numbers = ["15088603329","18758032593"]
	ding_text("75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494",text,numbers,False)

def getProcByName(name):
	# attrs = ['pid', 'memory_percent', 'name', 'cpu_times', 'create_time','memory_info']
	procRet = None
	attrs = ['pid', 'memory_percent', 'name', 'cpu_times','memory_info']
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
	if gb>1 :
		return str(round(gb,2))+"GB"
	else:
		return str(round(mb,2))+"MB"

def restart(cmd):
	# os.system(cmd)#会将标准输出到这里
	# subprocess.call(cmd)#不会将标准输出到这里
	pos = cmd.rfind("/")
	cwd = cmd[:pos]
	print(pos,cwd)
	if "Windows" == platform.system():
		subprocess.Popen(cmd,cwd=cwd)
	else:
		with open("/dev/null") as f:
			subprocess.Popen(cmd,stdout=f,cwd=cwd)

def tryRestart(name,cmd):
	p = multiprocessing.Process(target=restart, args=(cmd,))
	p.start()

	time.sleep(1)
	proc = getProcByName(name)
	return proc

def checkProc(name,restartCmd):
	text = ""
	proc = getProcByName(name)
	if not proc or not proc.is_running():
		text += "# Exe Warning\n"
		text += "The Exe="+name+" is not running!!!\n" \
		"#### try restart="+restartCmd+"\n"

		proc = tryRestart(name,restartCmd)
		text += "result = " + str((proc and proc.is_running())) + "\n"
	return text,proc

def worker(isProduction,thresholdCpu,thresholdAvailableMem,path,thresholdFreeeDisk,names,restartCmds):
	"""
	thresholdCpu cpu报警上限阈值
	thresholdAvailableMem 内存可用下限阈值
	path 指定路径位置
	thresholdFreeeDisk 指定路径的磁盘可用下限阈值
	names 指定检查的进程名字列表
	restartCmds 指定对应的重启命令列表
	"""
	t = type(names)
	arrayType = type([])
	print(t,t == arrayType)
	if type(names) != arrayType or type(restartCmds) != arrayType or len(names) != len(restartCmds):
		raise ValueError("need array")

	now = datetime.datetime.now()
	date = now.strftime('%Y-%m-%d %H:%M:%S')
	# print(now.ctime())
	curTime = str(date) + "." + str(now.microsecond) + "\n"
	print("working",curTime)
	text = curTime

	procs = []
	for i in range(len(names)):
		procText,proc = checkProc(names[i],restartCmds[i])
		text += procText
		if proc:
			procs.append(proc)
	
	if text == curTime:#所有程序都在正常运行
		# print(proc)
		# print(proc.exe())
		# print("cmdline=",proc.cmdline())
		# if "Windows" == platform.system():
		# 	print("num_handles=",proc.num_handles())
		# else:
		# 	print("num_fds=",proc.num_fds())
		# print("num_threads=",proc.num_threads())
		print("memory_info=",proc.memory_info())
		# print("memory_percent=",proc.memory_percent())
		# print("connections=",proc.connections())

		cpu = psutil.cpu_percent(interval=0.1)
		exeCpu = proc.cpu_percent(0.1)

		print(cpu,exeCpu)
		if(cpu > thresholdCpu):
			text += "# CPU Warning\n"
			text += "TOTAL CPU="+str(cpu)+" is over threshold("+str(thresholdCpu)+")."

			for i in range(procs):
				exeCpu = procs[i].cpu_percent(0.1)
				text += "["+names[i]+",cpu=]"+str(exeCpu)+"]"
			text += "\n"
		# print("*"*60)
		vm = psutil.virtual_memory()
		# print("virtual_memory=",type(vm), vm)
		# print("*"*60)
		# print("virtual_memory=",vm.total, vm.available, vm.percent)  # 查看虚拟内存
		if(vm.available < thresholdAvailableMem):
			text += "# Memory Warning\n"
			text += "TOTAL Memory Available="+getMbFromByte(vm.available)+" is under threshold(" \
			+getMbFromByte(thresholdAvailableMem)+")."

			for i in range(procs):
				proc = procs[i]
				text += "["+names[i]+" memory_percent="+str(round(proc.memory_percent(),2)) \
				+"%,rss(虚拟耗用内存)="+getMbFromByte(proc.memory_info().rss)+",vms(实际物理内存)=" \
				+getMbFromByte(proc.memory_info().vms)+"]"
			text += "\n"
			
		# print("*"*60)
		# print("disk_partitions=",psutil.disk_partitions())  # 查看硬盘分区
		# print("*"*60)
		pathDiskUsage = psutil.disk_usage(path)
		# print("disk_usage=",pathDiskUsage)  # 查看硬盘使用
		# print("*"*60)
		if(pathDiskUsage.free < thresholdFreeeDisk):
			text += "# Disk Warning\n"
			text += "Disk("+path+") Free="+getMbFromByte(pathDiskUsage.free) \
			+" is under threshold("+getMbFromByte(thresholdFreeeDisk)+")\n"
		# print("net_io_counters=",psutil.net_io_counters(pernic=True))  # 查看网络链接

	if text != curTime:
		if not isProduction:
			text += "## Test\n"

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

	print(sys.argv,len(sys.argv))

	IsProduction = False
	#@注意 路径必须以 / 分隔
	if len(sys.argv) >= 2 and sys.argv[1] == "production":
		IsProduction = True
		names = ["skynet","auth","xqtpay","slot","lottery"]
		cmds = ["/opt/fish/sh_start.sh"
		,"/opt/auth/start.sh","/opt/xqtpay/start.sh","/opt/slot/start.sh","/opt/lottery/start.sh"]
	else:
		names = ["tcpproxy","tcpproxy_test","skynet","auth","xqtpay","slot","lottery"]
		cmds = ["/opt/tcpproxy/start.sh","/opt/tcpproxy_test/start.sh","/opt/fish/sh_start.sh"
		,"/opt/auth/start.sh","/opt/xqtpay/start.sh","/opt/slot/start.sh","/opt/lottery/start.sh"]

	print(names)
	#测试服
	# worker(10,mb100,"/",mb100,["tcpproxy_test","skynet","auth","xqtpay","slot"]
	# 	,["/opt/fish/sh_start.sh"])
	# #正式服
	worker(IsProduction,10,mb100,"/home",mb1000,names,cmds)

	
	# checkProc("fishjs.exe","D:/glp/Github/Fish2/frameworks/runtime-src/proj.win32/Debug.win32/fishjs.exe")
	# checkProc("skynet","/opt/fish/sh_start.sh")

