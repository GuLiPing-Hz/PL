
import os

import sys
sys.path.append("..")
import file_helper

IMAGE_KEY = "key"

def optionJSRes5(path,file):
    if(".webp" not in file):
        return

    fullpath=file_helper.join(path,file)

    new_path = path.replace("/zhitu-des/webp","")
    new_path = new_path.replace("res1","res");
    new_file = file.replace(".webp",".png")
    new_fullpath = file_helper.join(new_path,new_file)
    print(fullpath,">>",new_fullpath)
    file_helper.move_file(fullpath,new_fullpath);

def encFile(path,file):

    if file[-4:] != ".png" and file[-5:] != ".webp" and file[-4:] != ".jsc":
        return

    fullpath=file_helper.join(path,file)
    print("cur file = ",fullpath)
    with open(fullpath,"rb+") as fp:
        data = fp.read()
        dataLen = len(data)
        #print(type(data))
        newData = bytearray(dataLen)#申明字节数组
        print("len = ",dataLen)
        for i in range(len(data)):
            
            #ord()函数主要用来返回对应字符的ascii码，ord('a') = 97
            #chr()主要用来表示ascii码对应的字符他的输入时数字，可以用十进制，也可以用十六进制 chr(97) = 'a'
            tempData = data[i] ^ ord(IMAGE_KEY[i%len(IMAGE_KEY)])
            #data[i] = tempData
            newData[i] = tempData
            #print("i=",i,",dataLen=",dataLen,"data=",data[i],"newData=",newData[i])

        #另存为
        # with open(fullpath+".copy","wb") as fp1:
        #   fp1.write(newData)
        #   fp1.flush()
        #保存到自己
        fp.seek(0)
        fp.write(newData)
        fp.flush()

def temp(path):
    #图片处理的一些列操作 后缀.webp改成.png

    #遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path,True).walk(optionJSRes5);
    #移除智图留下的残余文件
    file_helper.remove_dir(path+"/zhitu-des");
    #加密图片
    print("开始加密图片文件...")
    #临时文件加密
    file_helper.Diskwalk(path,False).walk(encFile);
    print("加密图片文件完成")

def main(path):
    #图片处理的一些列操作 后缀.webp改成.png

    #移除默认图片
    file_helper.remove_dir(path+"/res1/Default");
    #遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path+"/res1",True).walk(optionJSRes5);
    #移除智图留下的残余文件
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/platform/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/fishs/zhitu-des");
    #加密图片
    print("开始加密图片文件...")
    file_helper.Diskwalk(path+"/res",True).walk(encFile);
    print("加密图片文件完成")
    
def enc_jss(path):
    print("开始加密jsc文件...")
    file_helper.Diskwalk(path,True).walk(encFile);
    print("完成加密jsc文件...")

if __name__ == '__main__':
    #以后路径统一使用 '/ 请勿使用 '\\'
    
    #运行一次是加密，运行第二次是解密
    IMAGE_KEY = "aaazhejiangfanyu2018"

    # main("D:/glp/GitHub/fishjs")
    temp("D:/glp/work/UI/temp")

    #编译工程 最后一步，加密jsc，跟苹果斗智斗勇
    enc_jss("D:/glp/Github/fishjs/third_part/jsc/src")

    #热更新 jsc加密一下
    # enc_jss("D:/glp/work/temp/update/src")

    # encFile("D:/glp/work/UI/temp","jinbi5.png")
    
