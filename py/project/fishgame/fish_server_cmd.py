import platform
import os
#yum install python-devel
#yum install patch
#pip install readline #要使用readline必须安装上面的python开发包
import readline #引入该包可以再读取input的时候使用delete

#更新充值配置
#通知认证服务器
# curl -i http://127.0.0.1:32767/updateCfg?token=auth_notify
#更新金币配置
# curl -i http://127.0.0.1:56799/reloadGold

#服务器切换配置要一致。
PortCfg = 56799
FishCrontab = "crontab /opt/py/fish2.crontab"

def fish_server_cmd1():
	os.system("""
crontab -r
echo ****************************定时任务已关闭，请及时开启!!!!!!!!"""+FishCrontab+"""
date
curl -i http://127.0.0.1:"""+str(PortCfg)+"""/stopservice?sign=52a11abea3551c646001ae447329e74c
	""")

def fish_server_cmd2():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadMyCfg"
	print("cmd=",cmd)
	os.system(cmd)

def fish_server_cmd3():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadRoomConfig?type=3"
	print("cmd=",cmd)
	os.system(cmd)

def fish_server_cmd4():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/getData"
	print("cmd=",cmd)
	os.system(cmd)
	
def fish_server_cmd5():
	print("cmd=",FishCrontab)
	os.system(FishCrontab)

def fish_server_cmd6():
	cmd = "/opt/soft/redis-5.0.3/src/redis-server /opt/soft/redis-5.0.3/redis.conf"
	print("cmd=",cmd)
	os.system(cmd)

def fish_server_cmd7():
	#使用redis客户端查看服务器，并带上密码
	#/opt/soft/redis-5.0.3/src/redis-cli -a C9BE6E8D-F2CF-4154-BD34-922844BEAC11
	cmd = "/opt/soft/redis-5.0.3/src/redis-cli -a C9BE6E8D-F2CF-4154-BD34-922844BEAC11 shutdown"
	print("cmd=",cmd)
	os.system(cmd)

def fish_server_cmd8():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadUp"
	print("cmd=",cmd)
	os.system(cmd)
	# cmd = "curl -i http://127.0.0.1:56800/reloadUp"
	# print("cmd=",cmd)
	# os.system(cmd)

def fish_server_cmd9():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/stat"
	print("cmd=",cmd)
	os.system(cmd)

def fish_server_cmd10():
	cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/snapshot"
	print("cmd=",cmd)
	os.system(cmd)


def fish_server_cmd():
	strHelp ="""
捕鱼命令行,选择号码并回车：
	0.退出
	1.停服
	2.更新MyConf配置信息 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/reloadMyCfg
	3.更新房间配置 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/reloadRoomConfig?type=3
	4.查看当前在线人数 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/getData
	5.启用定时检查任务crontab
	6.开启redis
	7.关闭redis
	8.通知服务器充值配置变更
	9.查看当前服务器的STAT
	10.查看当前服务器的内存快照SNAPSHOT
"""
	print(strHelp)
	while(True):
		if "Windows" == platform.system():
			print("windows 不支持")
			break

		number = int(input("\n请输入："))
		print("number=",number)

		if number == 0:
			print("再见")
			break
		elif number == 1:
			number2 = int(input("\n确实要停止服务器吗?："))
			if number2 == 1:
				fish_server_cmd1()
			break
		elif number == 2:
			fish_server_cmd2()
		elif number == 3:
			fish_server_cmd3()
		elif number == 4:
			fish_server_cmd4()
		elif number == 5:
			fish_server_cmd5()
		elif number == 6:
			fish_server_cmd6()
		elif number == 7:
			fish_server_cmd7()
		elif number == 8:
			fish_server_cmd8()
		elif number == 9:
			fish_server_cmd9()
		elif number == 10:
			fish_server_cmd10()
		else:
			print(strHelp)

if __name__ == '__main__':
	fish_server_cmd()


