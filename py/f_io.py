#!python3.4
#@ guliping

"""
IO，标准IO，文件IO
"""

# 格式化字符串输出  str.format()
#str()： 函数返回一个用户易读的表达形式。
#repr()： 产生一个解释器易读的表达形式。
s1 = "Hello World\n"
print(str(s1),repr(s1))

for x in range(1, 3):
	print('{0:2d} {1:4d} {2:4d}'.format(x, x*x, x*x*x))
print("{0:.3f}".format(1.5))  # 类似c中的printf
print("{0:02d}".format(1))

# 位置参数与关键字参数
print("{0},{1}".format("apple","pen")) # 等价于print("{},{}".format("apple","pen"))
print("{1},{0}".format("apple","pen"))
print("{1},{0},{all}".format("apple","pen",all="applepen")) #关键字参数只能放在位置参数后面

table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
print('Runoob: {0[Runoob]:d}; Google: {0[Google]:d}; '
          'Taobao: {0[Taobao]:d}'.format(table))

# 需要在解释器环境中
#print("读取键盘读入")
#s2 = input("请输入：");
#print ("你输入的内容是: ", s2)

print("*"*60)

# 文件IO
"""
open(filename, mode)
filename：filename 变量是一个包含了你要访问的文件名称的字符串值。
mode：mode决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。
这个参数是非强制的，默认文件访问模式为只读(r)。
"""

f = open("zzz_io_test","w") # r rb r+ rb+ w wb w+ wb+ a ab a+ ab+
f.write("Hello World \n\tfrom python")
f.close()

f1 = open("zzz_io_test","r")
s3 = f1.read()  # f.read(size) siez 指定读取大小，如果没有传，读取文件全部内容
f1.close()
print("读取全部文件内容:",s3,repr(s3))

f2 = open("zzz_io_test","r")
s4 = f2.readline()
f2.close()
print("读取文件一行内容",s4)

f3 = open("zzz_io_test","r")
s5 = f3.readlines()
f3.close()
print("读取文件所有行",s5)

f4 = open("zzz_io_test","r")
for line in f4:
	print("循环读取文件行",line,end="") #读取的行内容带有换行符 \n
f4.close()
