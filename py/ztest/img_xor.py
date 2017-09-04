#!python 3.4
# 遍历cocos的图片文件 加密

import os
import shutil
import tempfile

gImgKey = ""

def copyFile(src_path,dst_path):
	# filename1 = tempfile.mktemp (".txt")
	open (dst_path, "w").close ()

	# if(os.path.isfile(dst_path)):
	# 	os.remove(dst_path)

	#dst_path = src_path + ".copy"
	print(src_path, "=>", dst_path)

	#拷文件
	shutil.copy (src_path, dst_path)
	if os.path.isfile (dst_path): 
		print(dst_path,"Copy Success")


def copyDir(src_path,dst_path):
	#拷贝目录
	#dirname1 = tempfile.mktemp (".dir")
	os.mkdir (dst_path)
	dst_path = src_path + ".copy"
	print(src_path, "=>", dst_path)

	shutil.copytree (src_path, dst_path)
	if os.path.isdir (dst_path): print(dst_path,"Copy Success")

def visitDir(path,func=None):
	retPaths=[]#文件路径列表
	retFiles = [];#文件名列表

	for dirpath,dirnames,filenames in os.walk(path):
		print("dirpath=",dirpath,",dirnames=",dirnames,",filenames=",filenames)

		for file in filenames:
			retFiles.append(file)
			fullpath=os.path.join(dirpath,file)
			retPaths.append(fullpath)

			if(func and callable(func)):
				func(dirpath,file)
	
	return retFiles,retPaths

def encFile(path,file):

	if file[-4:] != ".png" and file[-5:] != ".webp":
		return

	fullpath=os.path.join(path,file)
	print("cur file = ",fullpath,", gImgKey=",gImgKey)
	with open(fullpath,"rb+") as fp:
		data = fp.read()
		dataLen = len(data)
		#print(type(data))
		newData = bytearray(dataLen)#申明字节数组
		print("len = ",dataLen)
		for i in range(len(data)):
			
			tempData = data[i] ^ ord(gImgKey[i%len(gImgKey)])
			#data[i] = tempData
			newData[i] = tempData
			#print("i=",i,",dataLen=",dataLen,"data=",data[i],"newData=",newData[i])

		#另存为
		# with open(fullpath+".copy","wb") as fp1:
		# 	fp1.write(newData)
		# 	fp1.flush()
		#保存到自己
		fp.seek(0)
		fp.write(newData)
		fp.flush()
		

def main():

	#运行一次是加密，运行第二次是解密

	#gImgKey = "#ZGPani.com" 这里是局部变量
	print("开始加密图片文件...")
	visitDir("D:\\glp\\GitHub\\fishjs\\studio\\res\\enc",encFile)
	#visitDir("D:\\glp\\GitHub\\fishjsedit\\res\\games\\fish\\fishs",encFile)
	#encFile("D:\\glp\\GitHub\\fishlua\\simulator\\win32\\res\\test","HelloWorld.png")
	#encFile("D:\\glp\\GitHub\\fishlua\\simulator\\win32\\res\\test","HelloWorld.png.copy")
	print("加密图片文件完成")

if __name__ == '__main__':
	gImgKey = "#ZGPani.com"
	main()
