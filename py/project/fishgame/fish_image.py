
import os

import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper
import fish_hotupdate

IMAGE_KEY = "key"


def optionJSRes5(path, file):
    if(".webp" not in file):
        return

    fullpath = file_helper.join(path, file)

    new_path = path.replace("/zhitu-des/webp", "")
    new_path = new_path.replace("res1", "res")
    new_file = file.replace(".webp", ".png")
    new_fullpath = file_helper.join(new_path, new_file)
    print(fullpath, ">>", new_fullpath)

    file_helper.make_dirs(new_path)
    # file_helper.move_file(fullpath, new_fullpath)
    file_helper.copy_file(fullpath, new_fullpath)


def encFile(path, file):

    if file[-4:] != ".png" and file[-5:] != ".webp" and file[-4:] != ".jsc":
        return
    if(file == "loading.js"):
        return

    fullpath = file_helper.join(path, file)
    print("cur file = ", fullpath)
    with open(fullpath, "rb+") as fp:
        data = fp.read()
        dataLen = len(data)
        # print(type(data))
        newData = bytearray(dataLen)  # 申明字节数组
        print("len = ", dataLen)
        for i in range(len(data)):

            # ord()函数主要用来返回对应字符的ascii码，ord('a') = 97
            # chr()主要用来表示ascii码对应的字符他的输入时数字，可以用十进制，也可以用十六进制 chr(97) = 'a'
            tempData = data[i] ^ ord(IMAGE_KEY[i % len(IMAGE_KEY)])
            #data[i] = tempData
            newData[i] = tempData
            # print("i=",i,",dataLen=",dataLen,"data=",data[i],"newData=",newData[i])

        # 另存为
        # with open(fullpath+".copy","wb") as fp1:
        #   fp1.write(newData)
        #   fp1.flush()
        # 保存到自己
        fp.seek(0)
        fp.write(newData)
        fp.flush()


def png2Jpg(path,file):
    filePath = path + "/" + file
    newFilePath = filePath.replace(".png",".jpg")
    file_helper.move_file(filePath,newFilePath)

def temp(path, recursive=False):
    # 图片处理的一些列操作 后缀.webp改成.png

    # 遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path, True).walk(optionJSRes5)
    # 移除智图留下的残余文件
    file_helper.remove_dir(path+"/zhitu-des")
    # 加密图片
    print("开始加密图片文件...")
    # 临时文件加密
    file_helper.Diskwalk(path, recursive).walk(encFile)
    print("加密图片文件完成")


def main(path):
    # 图片处理的一些列操作 后缀.webp改成.png

    # 移除默认图片
    file_helper.remove_dir(path+"/res1/Default")
    # 遍历目录，取出智图软件处理后的webp图片，放到原来的位置，并重命名为png
    file_helper.Diskwalk(path+"/res1", True).walk(optionJSRes5)
    # 移除智图留下的残余文件
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/platform/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/zhitu-des");
    # file_helper.remove_dir("D:/glp/GitHub/fishjs/res1/games/fish/fishs/zhitu-des");
    # 加密图片
    print("开始加密图片文件...")
    file_helper.Diskwalk(path+"/res", True).walk(encFile)
    print("加密图片文件完成")


def enc_jss(path):
    print("开始加密jsc文件...")
    file_helper.Diskwalk(path, True).walk(encFile)
    print("完成加密jsc文件...")


def productGen(ver,dir,isTest=True,onlyVer=True):
    version = ver
    projectDir = dir
    if onlyVer:
        
        #打包整个项目
        

        file_helper.write_str_to_file(projectDir+"src/ver.js","""
var Ver = {
    version: """+repr(version)+"""//auto write by python
};
        """)
        print("Write ver.js")
        return

    # enc_jss("D:/glp/Github/fishjs/third_part/jsc/src")
    enc_jss(projectDir+"third_part/jsc/src")
    file_helper.remove_dir(projectDir+"third_part/jsc_ios/src");
    file_helper.copy_dir(projectDir+"third_part/jsc/src"
        ,projectDir+"third_part/jsc_ios/src");
    file_helper.remove_file(projectDir+"/third_part/jsc_ios/src/app.jsc")#ios目录不需要这个文件
    
    #release路径js替换成jsc
    file_helper.remove_dir(projectDir+"frameworks/runtime-src/proj.win32/Release.win32/script");
    file_helper.remove_dir(projectDir+"frameworks/runtime-src/proj.win32/Release.win32/src");
    try:
        file_helper.remove_file(projectDir+"frameworks/runtime-src/proj.win32/Release.win32/main.js")
    except Exception as e:
        pass
    try:
        file_helper.remove_file(projectDir+"frameworks/runtime-src/proj.win32/Release.win32/main_ios.js")
    except Exception as e:
        pass
    file_helper.copy_dir(projectDir+"third_part/jsc/script"
        ,projectDir+"frameworks/runtime-src/proj.win32/Release.win32/script");
    file_helper.copy_dir(projectDir+"third_part/jsc/src"
        ,projectDir+"frameworks/runtime-src/proj.win32/Release.win32/src");

    print(version+"更新包生成。。。")
    #然后执行manifest生成脚本
    fish_hotupdate.lailaifish_manifest_gen(version,True,isTest)

if __name__ == '__main__':
    # 以后路径统一使用 '/ 请勿使用 '\\'

    # 运行一次是加密，运行第二次是解密
    IMAGE_KEY = "aaazhejiangfanyu2018"  # 主包加密
    # IMAGE_KEY = "spzhejiangfanyu2018" #sp渠道加密

    # main("D:/glp/GitHub/Fish2")
    # 加密增加的图片文件
    # temp("D:/glp/work/UI/temp",False);#是否遍历子目录

    # 编译工程 最后一步，加密jsc，跟苹果斗智斗勇
    # enc_jss("D:/glp/Github/Fish2/third_part/jsc/1")#打包单独的jsc

    #第一步更改版本号，生成，版本文件，
    #第二步VS编译jsc文件
    #第三步再次执行我们的脚本文件
    version = "2.0.0.54" #2.0.0.53
    #打包整个项目
    projectDir = "D:/glp/Github/Fish2/"
    isTest = True
    # productGen(version,projectDir,isTest)
    productGen(version,projectDir,isTest,False)
    

    # enc_jss("D:/glp/Github/Fish2/third_part/jsc")
    # enc_jss("D:/glp/Github/Fish2/third_part/jsc_sp")//短信渠道包

    # 热更新 jsc加密一下
    # enc_jss("D:/glp/work/temp/update/src")

    # encFile("D:/glp/work/UI/temp","jinbi5.png")
