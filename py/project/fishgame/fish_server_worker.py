import datetime
# 查看系统运行状态 pip install psutil
# https://pypi.org/project/psutil/
import psutil

def worker():
	now = datetime.datetime.now()
	date = now.strftime('%Y-%m-%d %H:%M:%S')
	# print(now.ctime())
	time = str(date) + "." + str(now.microsecond)
	print("working",time)

	print("cpu=",psutil.cpu_percent())  # 查看CPU
	print("*"*60)
	vm = psutil.virtual_memory()
	print("virtual_memory=",type(vm), vm)
	print("*"*60)
	print("virtual_memory=",vm.total, vm.available, vm.percent)  # 查看虚拟内存
	print("*"*60)
	print("disk_partitions=",psutil.disk_partitions())  # 查看硬盘分区
	print("*"*60)
	print("disk_usage=",psutil.disk_usage('/'))  # 查看硬盘使用
	print("*"*60)
	print("net_io_counters=",psutil.net_io_counters(pernic=True))  # 查看网络链接

	attrs = ['pid', 'memory_percent', 'name', 'cpu_times', 'create_time',
             'memory_info']
	for proc in psutil.process_iter(attrs=attrs):
		print(proc.info)

if __name__ == '__main__':
	worker()

