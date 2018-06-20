import os
#当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
#然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
#正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append("..")
import file_helper
import json

"""
本文件是依赖python3

1.首先使用git拉出上个版本的分支
2.其次移出项目的编译目录[Debug.win32]中的[res,script,src]3个目录
3.记得用git还原一些项目mp3等文件(windows版本需) （这一步废弃了，，不需要还原了）
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
	update_dir = src_dir+"/../update"

	print(">> 删除原来的热更新目录")
	file_helper.remove_dir(new_dir)
	print(">> 创建新的目录")
	file_helper.make_dirs(new_dir)

	arra_a1 = []
	arra_b1 = []
	def src_func(dirpath,file):
		arra_a1.append(file_helper.join(dirpath[len(src_dir):],file))
	def dst_func(dirpath,file):
		arra_b1.append(file_helper.join(dirpath[len(dst_dir):],file))

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
		for x in [".lib",".exp",".gitignore",".pdb",".exe",".dll",".zip","main.js",".mp3",".bat",".jsc",".manifest"]:
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

	# return
	print(">> 开始拷贝文件")
	for i,v in enumerate(arra_c):
		print(">>",i,v,arra_c_to[i]);
		file_helper.copy_file(v,arra_c_to[i])

	print(">> 移除game_2")
	file_helper.remove_dir(new_dir+"/src/game/game_2_hide");
	print(">> 移除update目录")
	file_helper.remove_dir(new_dir+"/../update");

	print(">> 拷贝资源到热更新目录update")
	def copy_res_no_js(dirpath,file):
		# print("*"*100)
		# print(dirpath,file)
		if dirpath.startswith(new_dir+"/src"):#js 不用拷贝
			pass
		elif dirpath.startswith(new_dir+"/script"):#js 不用拷贝
			pass
		elif file == "jscompile.bat":
			pass
		else:#资源拷贝
			dirpath_new = dirpath.replace(new_dir,update_dir)
			# print(dirpath_new)
			file_helper.copy_file(file_helper.join(dirpath,file),file_helper.join(dirpath_new,file))
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
	jscompile_bat = file_helper.join(new_dir,"jscompile.bat")
	file_helper.write_str_to_file(jscompile_bat,text)
	print(">> 请手动改成python27,并双击",jscompile_bat)

	# js_compile_cmd = "cocos jscompile -s "+new_dir+"/src -d "+new_dir+"/../update"
	# os.system(js_compile_cmd) #cocos 脚本需要python27环境

	print(">> 脚本生成的 update 在上层目录中")
	print(">> 对jsc进行加密")
	print(">> 待脚本执行后，前往update目录，打包成最新版本的zip(当前版本是1.0.7,就是'1.0.7.zip'),这就是我们的更新包了,移除src和res目录")
	print(">> 执行本脚本中的createManifestEx函数，project.mainifest和version.manifest就生成了")

curAssetCnt = 0
def createManifestEx(manifest_file_pre,path,ver,ver_pre):
	try:
		with open(manifest_file_pre,"r") as file:
			manifest = json.load(file)
			print(manifest,type(manifest))

			project_manifest = "project_platform.manifest"
			version_manifest = "version_platform.manifest"

			url = manifest["packageUrl"]
			manifest["remoteManifestUrl"] = url+ver+"/"+project_manifest
			manifest["remoteVersionUrl"] = url+ver+"/"+version_manifest
			manifest["version"]=ver

			global curAssetCnt
			curAssetCnt = len(manifest["assets"])
			def walk_dir(path,file):
				full_path_file = path+"/"+file

				if(file.endswith(".js.map")):#解释文件不记录
					file_helper.remove_file(full_path_file)
					return
				if(file.endswith(".manifest")):#配置文件不记录
					return

				if(not file.endswith(".zip")):
					return

				global curAssetCnt
				print(curAssetCnt)
				# print(path,file);
				new_path_file = "update/"+file;
				print(new_path_file)

				# {"size":7418,"md5":"7551284fcba1c5543c0454526bb8991a"}
				asset = {
					"path": new_path_file,
					"md5": file_helper.md5_file(full_path_file),
					"compressed" : file.endswith(".zip"),
					"size": file_helper.file_size(full_path_file)}
				print(asset)

				curAssetCnt+=1
				update_asset_name = "update"+str(curAssetCnt)
				manifest["assets"][update_asset_name] = asset

			file_helper.Diskwalk(path).walk(walk_dir)

			path_update = path+"/../"+ver_pre
			file_helper.make_dirs(path_update)
			file_helper.write_str_to_file(path_update+"/"+project_manifest,json.dumps(manifest,indent=0,sort_keys=False));

			del manifest["assets"]
			del manifest["searchPaths"]
			file_helper.write_str_to_file(path_update+"/"+version_manifest,json.dumps(manifest,indent=0,sort_keys=False));

			path_cur = path+"/../"+ver
			file_helper.remove_dir(path_cur)
			file_helper.copy_dir(path_update,path_cur)

	except FileNotFoundError:
		print(manifest_file_pre+" FileNotFoundError")
		pass

def creatLobbyManifest(ver_pre,version,url,src,dest,next=False):
	url_pre = url+ver_pre+"/"
	manifest = {
	    "packageUrl": url_pre,
	    "remoteManifestUrl": url_pre+"project.manifest",
	    "remoteVersionUrl": url_pre+"version.manifest",
	    "version": ver_pre,
	    "assets": {},
	    "searchPaths": []#"update"
	};

	def walk_dir(path,file):
		full_path_file = path+"/"+file

		if(file.endswith(".js.map")):#解释文件不记录
			file_helper.remove_file(full_path_file)
			return
		if(file.endswith(".manifest")):#配置文件不记录
			return;

		# print(path,file);
		new_path_file = path[len(src)+1:]+"/"+file;
		print(new_path_file)

		# {"size":7418,"md5":"7551284fcba1c5543c0454526bb8991a"}
		asset = {
			"path": new_path_file,
			"size": file_helper.file_size(full_path_file),
			"md5": file_helper.md5_file(full_path_file),
			"compressed" : file.endswith(".zip")}
		print(asset)

		manifest["assets"][new_path_file] = asset

	#遍历脚本目录
	file_helper.Diskwalk(src+"/src").walk(walk_dir)
	#遍历资源目录
	file_helper.Diskwalk(src+"/res").walk(walk_dir)

	cur_manifest_file_src = dest+"/assets/resources/project.manifest"
	cur_manifest_file_dest = src+"/res/raw-assets/resources/project.manifest"
	# if(force or not file_helper.is_file_exits(cur_manifest_file_src)):
	# creator 工程目录
	file_helper.write_str_to_file(cur_manifest_file_src,json.dumps(manifest,indent=0,sort_keys=False));
	# creator jsb 导出目录
	file_helper.write_str_to_file(cur_manifest_file_dest,json.dumps(manifest,indent=0,sort_keys=False));

	print("当前项目资源生成完毕："+ver_pre);

	if(next):#是否生成下个版本的资源
		url_next = url+version+"/"
		print("url_next = "+url_next)

		# manifest["packageUrl"] = url_next #资源下载地址在上个版本的目录
		manifest["remoteManifestUrl"] = url_next+"project.manifest"  #,这里增加逗号，会表示这是一个数组
		manifest["remoteVersionUrl"] = url_next+"version.manifest"
		manifest["version"] = version #改成新版本
		dest_dir = dest+"/remote-assets/"+ver_pre
		print("dest_dir = "+dest_dir);

		file_helper.remove_dir(dest_dir)
		file_helper.copy_dir(src+"/src",dest_dir+"/src")
		file_helper.copy_dir(src+"/res",dest_dir+"/res")

		file_helper.write_str_to_file(dest_dir+"/project.manifest",json.dumps(manifest,indent=0,sort_keys=False));

		del manifest["assets"]
		del manifest["searchPaths"]
		file_helper.write_str_to_file(dest_dir+"/version.manifest",json.dumps(manifest,indent=0,sort_keys=False));

		print("热更新版更新资源生成完毕："+version);

def createGameManifest(game_id,url,ver,game_dir,src,dest,need_first=True):

	game_pro_manifest_name = "project_game_"+str(game_id)+".manifest"
	game_ver_manifest_name = "version_game_"+str(game_id)+".manifest"

	manifest = {
	    "packageUrl": url,
	    "remoteManifestUrl": url+game_pro_manifest_name,
	    "remoteVersionUrl": url+game_ver_manifest_name,
	    "version": "1.0.0",
	    "assets": {},
	    "searchPaths": []#"update"
	};

	if(need_first):	
		cur_manifest_file_src = dest+"/assets/resources/"+game_pro_manifest_name
		cur_manifest_file_dest = src+"/res/raw-assets/resources/"+game_pro_manifest_name
		# if(force or not file_helper.is_file_exits(cur_manifest_file_src)):
		# creator 工程目录
		print("cur_manifest_file_src ="+cur_manifest_file_src)
		file_helper.write_str_to_file(cur_manifest_file_src,json.dumps(manifest,indent=0,sort_keys=False));
		# creator jsb 导出目录
		file_helper.write_str_to_file(cur_manifest_file_dest,json.dumps(manifest,indent=0,sort_keys=False));

	def walk_dir(path,file):
		full_path_file = path+"/"+file

		if(file.endswith(".js.map")):#解释文件不记录
			file_helper.remove_file(full_path_file)
			return
		if(file.endswith(".manifest")):#配置文件不记录
			return;

		# print(path,file);
		new_path_file = ""
		if(path == game_dir):
			new_path_file = file;
		else:
			new_path_file = path[len(game_dir)+1:]+"/"+file;
		print(new_path_file)

		# {"size":7418,"md5":"7551284fcba1c5543c0454526bb8991a"}
		asset = {
			"path": new_path_file,
			"size": file_helper.file_size(full_path_file),
			"md5": file_helper.md5_file(full_path_file),
			"compressed" : file.endswith(".zip")}
		print(asset)

		manifest["assets"][new_path_file] = asset

	#遍历脚本目录
	file_helper.Diskwalk(game_dir).walk(walk_dir)

	manifest["version"] = ver #改成新版本

	game_manifest_dir = game_dir#[0:game_dir.rfind("/")]
	print("game_manifest_dir = "+game_manifest_dir)
	# return 
	file_helper.write_str_to_file(game_manifest_dir+"/"+game_pro_manifest_name,json.dumps(manifest,indent=0,sort_keys=False));

	del manifest["assets"]
	del manifest["searchPaths"]
	file_helper.write_str_to_file(game_manifest_dir+"/"+game_ver_manifest_name,json.dumps(manifest,indent=0,sort_keys=False));

	print("游戏热更新资源生成完毕："+ver);

	if(need_first):
		print("第一版游戏资源生成完毕")

def lailaifish_manifest_gen():
	#公司电脑
	# main("D:/glp/work/temp/fishjs","D:/glp/GitHub/fishjs/frameworks/runtime-src/proj.win32/Debug.win32")

	#家里
	# main("D:/work/temp/fishjs","D:/work/GitHub/fishjs/frameworks/runtime-src/proj.win32/Debug.win32")
	
	#生成捕鱼更新包 manifest
	manifest_file_pre = "D:/glp/Github/fishjs/third_part/update/v1.0.7/1.0.6/project_platform.manifest"
	createManifestEx(manifest_file_pre,"D:/glp/work/temp/update","1.0.7","1.0.6")

if __name__ == '__main__':
	#以后路径统一使用 '/ 请勿使用 '\\'

	#来来捕鱼更新包配置文件
	lailaifish_manifest_gen();

	"""
		额。。。有点繁琐，先这样吧。。

		首次运行需要自己创建一个简单的manifest放到工程中

		1 creator构建 把修改的资源发布到目录
		2 运行脚本 读取修改的资源，修改project.manifest的内容
	"""
	# dir_src = "D:/glp/Github/CreatorTest/build/jsb-default"
	# dir_dest = "D:/glp/Github/CreatorTest"
	# package_url = "http://192.168.0.18:8080/CreatorTest/"

	# ver_pre = "1.0.0" #生成之前版本的更新包，所以我们创建的更新目录是之前版本的
	# ver_cur = "1.0.2"
	# is_creat_update_package = False
	# #创建大厅更新包
	# creatLobbyManifest(ver_pre,ver_cur,package_url+"remote-assets/",dir_src,dir_dest,is_creat_update_package);

	# game_dir = "D:/glp/Github/CreatorTest/CreatorGame/Game1/build/jsb-default/child-game"
	# game_id = 1
	# game_ver = "1.0.1"
	# childgame_package_url = package_url+"child-game/"
	#创建子游戏更新包
	# createGameManifest(game_id,childgame_package_url,game_ver,game_dir,dir_src,dir_dest,True)
