import os
#当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
#然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
#正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append("..")
import file_helper

"""
本文件是依赖python3

1.首先使用git拉出上个版本的分支
2.其次移出项目的编译目录[Debug.win32]中的[res,script,src]3个目录
3.记得用git还原一些项目mp3等文件(windows版本需)
4.使用vs编译项目工程,移动[res,script,src]目录和[main.js,project.json]文件至源目录src_dir
5.拉出最新的版本，同样是vs编译项目
6.使用本脚本拉出需要热更新的文件,
7.双击jscompile.bat编译jsc文件
8.修改project_platform.manifest 注意json数组的逗号, forceUpdate 设置为false,自己先测试一下,如果没问题然后再上传
9.上传文件,记得保存备份

遍历两个目录,获取到所有文件列表 数组A 和 数组B

A 代表上一个版本
B 代表当前的版本

遍历 B -> 某一文件
在A中没有: 				放入数组C
在A中有,MD5不一致: 		放入数组C
"""

def main(src_dir,dst_dir):
	new_dir = src_dir+"_hotupdate"
	update_dir = src_dir+"\\..\\update"

	print(">> 删除原来的热更新目录")
	file_helper.remove_dir(new_dir)
	print(">> 创建新的目录")
	file_helper.make_dirs(new_dir)

	arra_a1 = []
	arra_b1 = []
	def src_func(dirpath,file):
		arra_a1.append(os.path.join(dirpath[len(src_dir):],file))
	def dst_func(dirpath,file):
		arra_b1.append(os.path.join(dirpath[len(dst_dir):],file))

	arra_temp_a1, arra_a2 = file_helper.Diskwalk(src_dir).walk(src_func)
	arra_temp_b1, arra_b2 = file_helper.Diskwalk(dst_dir).walk(dst_func)

	# print(arra_temp_a1)
	# # print("*"*100)
	# # print(arra_a1)
	# # print("*"*100)
	# # print(arra_a2)
	# # return
	# print("*"*100)
	# print(arra_b1)
	# return

	arra_c = []
	for i,b1 in enumerate(arra_b1):
		#print(">>",i,b1)
		# filterLst = [b1.endswith(x) for x in [".lib",".exp",".gitignore",".pdb",".exe",".dll"]];
		# if True in filterLst:
		# 	continue

		filter = False
		for x in [".lib",".exp",".gitignore",".pdb",".exe",".dll",".zip","main.js",".mp3",".bat",".jsc"]:
			if b1.endswith(x):
				filter = True;
				break;

		if filter:
			#print("continue")
			continue

		file_b = arra_b2[i]
		if b1 in arra_a1:
			file_a = arra_a2[arra_a1.index(b1)]
			
			md5_a = file_helper.md5_file(file_a)
			md5_b = file_helper.md5_file(file_b)
			# print(file_a ," == " ,file_b)
			# print(md5_a ," == " ,md5_b ,md5_a == md5_b)

			if md5_a != md5_b:
				print(">> Modi append file ",file_b)
				print(file_a ," <==> " ,file_b)
				print(md5_a ," == " ,md5_b ,md5_a == md5_b)
				arra_c.append(file_b)
		else:
			print(">> New  append file ",file_b)
			arra_c.append(file_b)

	# print(">> 源文件展示")
	# print(arra_c)

	arra_c_to = [ x.replace(dst_dir,new_dir) for x in arra_c ]
	# print(">> 目标文件展示")
	# print(arra_c_to)

	print(">> 开始拷贝文件")
	for i,v in enumerate(arra_c):
		#print(">>",i,v);
		file_helper.copy_file(v,arra_c_to[i])

	print(">> 移除game_2")
	file_helper.remove_dir(new_dir+"\\src\\game\\game_2_hide");
	print(">> 移除update目录")
	file_helper.remove_dir(new_dir+"\\..\\update");

	print(">> 拷贝资源到热更新目录update")
	def copy_res_no_js(dirpath,file):
		# print("*"*100)
		# print(dirpath,file)
		if dirpath.startswith(new_dir+"\\src"):#js 不用拷贝
			pass
		elif dirpath.startswith(new_dir+"\\script"):#js 不用拷贝
			pass
		elif file == "jscompile.bat":
			pass
		else:#资源拷贝
			dirpath_new = dirpath.replace(new_dir,update_dir)
			# print(dirpath_new)
			file_helper.copy_file(os.path.join(dirpath,file),os.path.join(dirpath_new,file))
	file_helper.Diskwalk(new_dir).walk(copy_res_no_js)
	print(">> 写入JS加密脚本 需要python27")

	text = """	
echo 当前盘符：%~d0
echo 当前路径：%cd%
echo 当前执行命令行：%0
echo 当前bat文件路径：%~dp0
echo 当前bat文件短路径：%~sdp0

%~d0
cd %~dp0
cocos jscompile -s . -d ../update
		"""
	jscompile_bat = os.path.join(new_dir,"jscompile.bat")
	file_helper.write_str_to_file(jscompile_bat,text)
	print(">> 请手动改成python27,并双击",jscompile_bat)
	#os.system(jscompile_bat) cocos 脚本需要python27环境
	print(">> 脚本生成的 update 在上层目录中")


if __name__ == '__main__':
	#公司电脑
	main("D:\\glp\\work\\temp\\fishjs","D:\\glp\\GitHub\\fishjs\\frameworks\\runtime-src\\proj.win32\\Debug.win32")

	#家里
	# main("D:\\work\\temp\\fishjs","D:\\work\\GitHub\\fishjs\\frameworks\\runtime-src\\proj.win32\\Debug.win32")
	

