import file_helper
import os

"""
1.首先使用git 拉出上个版本的分支,放到指定目录,指定当前版本的目录,
2.其次使用vs 编译项目工程,
3.使用本脚本拉出需要热更新的文件,
4.双击jscompile.bat编译jsc文件
5.修改project_platform.manifest 注意json数组的逗号, forceUpdate 设置为false,自己先测试一下,如果没问题然后再上传
6.上传文件,记得保存备份

遍历两个目录,获取到所有文件列表 数组A 和 数组B

A 代表上一个版本
B 代表当前的版本

遍历 B -> 某一文件
在A中没有: 				放入数组C
在A中有,MD5不一致: 		放入数组C
"""

def main(src_dir,dst_dir):
	newDir = src_dir+"_hotupdate"

	print(">> 删除原来的目录")
	file_helper.remove_dir(newDir)
	print(">> 创建新的目录")
	file_helper.make_dir(newDir)

	arra_a1, arra_a2 = file_helper.Diskwalk(src_dir).walk()
	arra_b1, arra_b2 = file_helper.Diskwalk(dst_dir).walk()

	# print(arra_a1)
	# print("*"*100)
	# print(arra_b1)
	#return

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
			#print(file_a ," == " ,file_b)
			#print(md5_a ," == " ,md5_b ,md5_a == md5_b)

			if md5_a != md5_b:
				print(">> Modi append file ",file_b)
				print(file_a ," <==> " ,file_b,md5_a ," == " ,md5_b ,md5_a == md5_b)
				arra_c.append(file_b)
		else:
			print(">> New  append file ",file_b)
			arra_c.append(file_b)

	# print(">> 源文件展示")
	# print(arra_c)

	arra_c_to = [ x.replace(dst_dir,newDir) for x in arra_c ]
	# print(">> 目标文件展示")
	# print(arra_c_to)

	print(">> 开始拷贝文件")
	for i,v in enumerate(arra_c):
		#print(">>",i,v);
		file_helper.copy_file(v,arra_c_to[i])

	print(">> 移除game_2")
	file_helper.remove_dir(newDir+"\\src\\game\\game_2_hide");

	print(">> 写入JS加密脚本 需要python27")

	text = """	
echo 当前盘符：%~d0
echo 当前路径：%cd%
echo 当前执行命令行：%0
echo 当前bat文件路径：%~dp0
echo 当前bat文件短路径：%~sdp0

%~d0
cd %~dp0
cocos jscompile -s . -d ../jsc
		"""
	jscompile_bat = os.path.join(newDir,"jscompile.bat")
	file_helper.write_str_to_file(jscompile_bat,text)
	print(">> 请手动双击",jscompile_bat)
	#os.system(jscompile_bat) cocos 脚本需要python27环境


if __name__ == '__main__':
	main("D:\\glp\\work\\temp\\fishjs"
		,"D:\\glp\\GitHub\\fishjs\\frameworks\\runtime-src\\proj.win32\\Debug.win32")
