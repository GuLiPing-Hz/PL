#python3

import os
import hashlib
import shutil
import tempfile
import zipfile

def join(path, new_file):
    return path+"/"+new_file

class Diskwalk(object):
    def __init__(self, path, recursive=True):
        """ 
                构造函数 
                @path 		指定目录
                @recursive 	是否遍历子目录
        """
        self.path = path
        self.recursive = recursive

    def walk(self, func=None):
        """ 
                遍历目录和文件
                @func 		指定回调, 回传当前路径和文件

                @return 	返回 文件名数组,全路径文件名数组  一一对应
        """
        path_collection = []
        files = []
        for dirpath, dirnames, filenames in os.walk(self.path):

            # print("dirpath=",dirpath)
            # print("dirnames=",dirnames)
            # print("filenames=",filenames)

            for file in filenames:
                dirpath = dirpath.replace("\\", "/")
                if(func and callable(func)):
                    func(dirpath, file)

                files.append(file)
                # fullpath=os.path.join(dirpath,file)
                fullpath = join(dirpath, file)
                path_collection.append(fullpath)

            if(not self.recursive):
                break

        return files, path_collection

    def walk_dir(self, func=None):
        """ 
                遍历目录不遍历文件
                @func 		指定回调, 回传当前路径和文件

                @return 	返回 所有子目录
        """
        path_collection = []
        for dirpath, dirnames, filenames in os.walk(self.path):

            # print("dirpath=",dirpath)
            # print("dirnames=",dirnames)
            # print("filenames=",filenames)

            dirpath = dirpath.replace("\\", "/")
            for dirname in dirnames:
                if(func and callable(func)):
                    func(dirpath, dirname)

                fullpath = join(dirpath, dirname)
                path_collection.append(fullpath)

            if(not self.recursive):
                break

        return path_collection

def MergeToOneDir(src_dir,dest_dir):
    def make_dirs(dir):
        """
                依次创建父子目录
        """
        try:
            print("makedirs dir =>", dir)
            os.makedirs(dir)
        except FileExistsError:  # 异常捕获
            pass

    first_dirs = Diskwalk(src_dir,False).walk_dir()
    print(first_dirs)
    for i in range(len(first_dirs)):
        zip_name = first_dirs[i].replace(src_dir,"")+".zip"
        zip_name = zip_name[1:]
        print(zip_name)

        _,files = Diskwalk(first_dirs[i]).walk(None)
        # print(files)

        with zipfile.ZipFile(join(dest_dir,zip_name), 'w') as myzip:
            for j in range(len(files)):
                file = files[j]
                file_name = file.replace(src_dir,"")
                file_name = file_name[1:].replace("/",".")
                file_name = file_name[:file_name.rfind(".")]
                print(zip_name," <- ",file,file_name)
                #指定压缩哪个文件，指定压缩文件中的目录名称
                myzip.write(file,file_name)


if __name__ == '__main__':
    MergeToOneDir("D:/glp/cocos/luaenc","D:/glp/cocos/luaenc_")

    


