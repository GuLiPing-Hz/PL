import os,sys


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
        	return files,path_collection

if __name__ == '__main__':

	#sys.argv[1]
	total = diskwalk("D:\\glp\\GitHub\\Fish\\res\\seafish").paths()
	file = total[0]
	path = total[1]

	for f in file:
		print(f.replace(".","_")+":"+'"res/seafish/'+f+'",')
