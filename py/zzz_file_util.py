#!python 3.6

import os
import sys
import shutil
import tempfile

def copyFile(src_path,dst_path):
	# filename1 = tempfile.mktemp (".txt")

	try:
		pos_1 = dst_path.find("/")
		pos_2 = dst_path.find("\\")
		pos = max(pos_1,pos_2)
		dir_dir = dst_path[0:pos]

		os.makedirs(dir_dir) #只能创建目录
	except FileExistsError:
		pass
	open (dst_path, "w").close ()

	#dst_path = src_path + ".copy"
	print(src_path, "=>", dst_path)

	#拷文件
	shutil.copy (src_path, dst_path)
	if os.path.isfile (dst_path): 
		print(dst_path,"Copy Success")

class diskwalk(object):
	def __init__(self,path):
		self.path = path
	def paths(self):
		path=self.path
		path_collection=[]
		files = [];
		for dirpath,dirnames,filenames in os.walk(path):
			for file in filenames:
				

				files.append(file)
				fullpath=os.path.join(dirpath,file)
				path_collection.append(fullpath)

				pos_end = file.find(".png");
				number = int(file[pos_end-2:pos_end])
				number += 1
				str_number = "{:02d}".format(number)
				# print("str_number=",str_number);

				new_path = file[0:pos_end-2]+str_number+".png"
				print(file,">>",new_path);
				new_full_path = os.path.join(dirpath,"new/"+new_path)
				# print("new_full_path=",new_full_path)
				copyFile(fullpath,new_full_path)
		
		return files,path_collection

if __name__ == '__main__':

	#遍历目录改文件名
	#C:\Users\JJ\Desktop\LF_boss_fish_PList.Dir
	total = diskwalk("C:\\Users\\JJ\\Desktop\\LF_boss_fish_PList.Dir").paths()
	# file = total[0]
	# path = total[1]

	# for f in file:
	# 	print(f.replace(".","_")+":"+'"res/seafish/'+f+'",')


