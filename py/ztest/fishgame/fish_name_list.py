#!python 3.6

from xml.etree import ElementTree
import os

#当我们脚本是主入口的时候,如果要引入上层目录的脚本,那么只能通过添加sys.path的方式
#然后并不推荐这样写,这样是由于设计目录的时候原本就不规范导致
#正确的方法应该是把我们自己写的脚本都放到一个目录，并且子目录的脚本不能引用上级目录的模块
import sys
sys.path.append("..")
import file_helper


def optionRename(path,file):
	fullpath=os.path.join(path,file)

	pos_end = file.find(".png");
	number = int(file[pos_end-2:pos_end])
	number += 1
	str_number = "{:02d}".format(number)
	# print("str_number=",str_number);

	new_path = file[0:pos_end-2]+str_number+".png"
	print(file,">>",new_path);
	new_full_path = os.path.join(path,"new/"+new_path)
	# print("new_full_path=",new_full_path)
	file_helper.copy_file(fullpath,new_full_path)

def optionRenameFishId(path,file):
	fullpath=os.path.join(path,file)

	new_file = file.replace("fish_27","fish_32");
	new_path = os.path.join(path,new_file);
	print(fullpath,">>",new_path);
	file_helper.move_file(fullpath,new_path)

def optionJSRes1(path,file):
	if("ignore" in path or file.startswith("particle_") or file.startswith("Plist")):
		return ;
	path_new = path[path.find("res"):].replace("\\","/")+"/"
	# print(path_new)

	name = file.replace(".","_");
	ext_file = file.replace(".png","");

	is_png = False;
	if("_png" in name):
		is_png = True;

	if("_webp" in name):
		is_png = True;
		name = name.replace("_webp","_png");
		ext_file = file.replace(".webp","");

	if(is_png):
		print(name+": '"+path_new+ext_file+"' + cfgImageExt,");#games/fish ; platform
	else:
		print(name+": '"+path_new+ext_file+"',");#games/fish ; platform

def optionJSRes1_(path,file):
	name = file.replace(".","_");

	if("_webp" in name):
		name = name.replace("_webp","_png");
	print("music_"+name+": 'res/games/fish/ogg/"+file+"',");#games/fish ; platform

def optionJSRes2(path,file):
	name = file.replace(".","_");
	print("'res/games/fish/fishs/"+file+"',");

def optionJSRes3(path,file):
	# if(file.find(".png") != -1):
	name = file.replace(".","_");

	if("_webp" in name):
		name = name.replace("_webp","_png");
	print(name+": 'res/games/fish/"+file+"',");

	if("ignore" in path):
		return ;
	path_new = path[path.find("res"):].replace("\\","/")+"/"
	# print(path_new)

	name = file.replace(".","_");
	ext_file = file.replace(".png","");

	is_png = False;
	if("_png" in name):
		is_png = True;

	if("_webp" in name):
		is_png = True;
		name = name.replace("_webp","_png");
		ext_file = file.replace(".webp","");

	if(is_png):
		print(name+": '"+path_new+ext_file+"' + cfgImageExt,");#games/fish ; platform
	else:
		print(name+": '"+path_new+ext_file+"',");#games/fish ; platform

#修改plist文件的纹理为png->webp
def optionJSRes4(path,file):
	plist_filename = path+"\\"+file;
	print(plist_filename);

	if("webp" in path):
		return

	if(".plist" in file and file.startswith("Plist")):
		tree = ElementTree.parse(plist_filename)
		root = tree.getroot()
		#root = ElementTree.fromstring(content.decode("utf-8"));
		print(root.tag,root.attrib,"text=",root.text);

		# for child in root:
		# 	print(child.tag, child.attrib,"text=",child.text);

			# for cc in child:
				# print(cc.tag, cc.attrib,"text=",cc.text);
			# cc = child[2];
			# print(cc.tag, cc.attrib,"text=",cc.text);

		child = root[0];
		
		cc = child[3];
		print(cc.tag, cc.attrib,"text=",cc.text);

		textureFileName = cc[3];
		#print("textureFileName:",textureFileName.tag, textureFileName.attrib,"text=",textureFileName.text,type(textureFileName.text));
		textureFileName.text = textureFileName.text.replace(".png",".webp");

		realTextureFileName = cc[5];
		#print(realTextureFileName.tag, realTextureFileName.attrib,"text=",realTextureFileName.text);
		realTextureFileName.text = realTextureFileName.text.replace(".png",".webp");
		#print("realTextureFileName:",realTextureFileName.tag, realTextureFileName.attrib,"text=",realTextureFileName.text);

		newFilePath = path+"\\webp";
		try:
			os.mkdir(newFilePath)
		except FileExistsError: #异常捕获
			pass

		tree.write(newFilePath+"\\"+file);

def optionCPP(path,file):
	if file.find(".c") != -1 or file.find(".cpp") != -1:
		print("../../../Classes/app/"+file)

if __name__ == '__main__':

	#print(file_helper)
	#遍历目录改文件名
	#C:\Users\JJ\Desktop\LF_boss_fish_PList.Dir
	#total = file_helper.Diskwalk("C:\\Users\\JJ\\Desktop\\LF_boss_fish_PList.Dir").walk(optionRename);
	# file = total[0]
	# path = total[1]

	#C++文件列表
	#file_helper.Diskwalk("D:\\glp\\GitHub\\LongConnectionTCP\\src\\Classes\\app",False).walk(optionCPP);
	#平台 图片文件 
	file_helper.Diskwalk("D:\\glp\\GitHub\\fishjs\\res\\platform").walk(optionJSRes1);
	#音频文件
	#file_helper.Diskwalk("D:\\glp\\GitHub\\fishjs\\res\\games\\fish\\ogg",False).walk(optionJSRes1_);
	#捕鱼 游动plist文件
	# file_helper.Diskwalk("D:\\glp\\GitHub\\fishjs\\studio\\res\\games\\fish\\fishs",False).walk(optionJSRes2);
	#捕鱼图片文件
	# file_helper.Diskwalk("D:\\glp\\GitHub\\fishjs\\res\\games\\fish",False).walk(optionJSRes1);	

	#鱼图片文件名字修改
	#file_helper.Diskwalk("D:\\glp\\work\\UI\\20170919\\package\\fishs",False).walk(optionRenameFishId);

	def water_name(path,file):#change 1
		print(path,file);
		os.rename(path+"\\"+file,path+"\\"+"water_"+file);

	# file_helper.Diskwalk("C:\\Users\\JJ\\Desktop\\png",False).walk(water_name);	
