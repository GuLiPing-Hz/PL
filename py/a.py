#!python3.4.2
'''
查询python环境
import builtins
dir(builtins)#跟lua一样，查看当前内建的变量和函数，模块
dir()#查看当前定义的变量,函数,模块
import sys
dir(sys)#查看该sys包下可用的变量，函数，模块
'''

'''
基础篇， 初识python
print 和 type都是 python内建的函数。
初识python类型和运算符

help函数可以给我们提供帮助文档

http://blog.csdn.net/glp3329/article/details/52511855
'''
'''
import keyword
keyword.kwlist

控制台输入，获取当前python的关键字

'''

# 单行注释
'''
多行注释 ， python讲究代码块的缩进保持一致
'''

#type(a)  不能使用未定义的变量

''' 输出
#Traceback (most recent call last): 
#  File "<stdin>", line 1, in <module> type(a) 
#NameError: name 'a' is not defined
'''

a = "123"
print(type(a)) # 输出 <class 'str'>
print(id(a)) # 输出 35672112 - 每个人的结果不一样
a = 12
print(type(a)) # 输出 <class 'int'>
print(id(a)) # 输出 1488898480 - 每个人的结果不一样
a = 12.3
print(type(a)) # 输出 <class 'float'>
print(id(a)) # 输出 5734688 - 每个人的结果不一样

'''
Python3 中有六个标准的数据类型:

Number（数字） int、float、bool、complex 
	只有一种整数类型 int，表示为长整型，没有 python2 中的 Long
String（字符串）
List（列表）
Tuple（元组）
Sets（集合）
Dictionary（字典）

申明的变量，可以使用del语句删除一些对象引用
del a, b
'''

'''作死除法
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
'''
#0/0

'''
python操作符

在交互模式下，python会把运算的结果保存在 '_' 里面
'''

# 1.算术运算符:
a = 10
b = 20
print("a+b=",a+b) #加
print("a-b=",a-b) #减
print("a*b=",a*b) #乘
print("b/a=",b/a) #除
print("b%a=",b%a) #模
print("b**a=",b**a) #指数
print("b//a=",b//a) #地板除 取整
print("-a=",-a)
print("*"*30)

# 2.比较操作符:
print("a==b",a==b)
print("a!=b",a!=b)
print("a>b",a>b)
print("a<b",a<b)
print("a>=b",a>=b)
print("a<=b",a<=b)

# 3.赋值运算符：
c = 1;
c += a
print("c+=a = ",c)
c -= a
print("c-=a = ",c)

#类似的还有 *= /= %= **= //=
c *= 2
print(c)
c /= 2
print(c)
c %= 1
print(c)
c **= 2
print(c)
c //= 2
print(c)

# 4.位运算符：
a = 3 #二进制的表示  0000 0011
b = 10 #二进制的表示 0000 1010

print("a&b =",a&b) #按位与
print("a|b =",a|b) #按位或
print("a^b =",a^b) #按位异或
print("~b =",~b) #按位取反
print("a<<2 =",a<<2) #按位左移
print("b>>2 =",b>>2) #按位右移

# 5.逻辑运算符:
a = True # 这里必须大写
b = False
print(a and b) 	#等价与 &&
print(a or b) 	#等价与 ||
print(not a) 	#等价与 !

# 6.成员运算符:
a = "a"
b = "abcdefg"
print("a in b =",a in b) #判断a是否在b的里面，可以是字符串，或者是元组，序列，字典
print("a not in b =",a not in b)

# 7.身份运算符
a = 1
b = 2
print("a is b =",a is b) #判断是否同一个对象
print("a is not b =",a is not b)
b = 1
print("a is b =",a is b)

"""

Python运算符优先级
以下表格列出了从最高到最低优先级的所有运算符：
运算符				描述
**					指数 (最高优先级)
~ + -				按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@)
* / % //			乘，除，取模和取整除
+ -					加法减法
>> <<				右移，左移运算符
&					位 'AND'
^ |					位运算符
<= < > >=			比较运算符
<> == !=			等于运算符
= %= /= //= -= += *= **=	赋值运算符
is is not			身份运算符
in not in			成员运算符
not or and			逻辑运算符

"""

#字符串连接符 +
print("123"+"abc")

'''
需要说明的是 python不支持字符串和数字相加，lua可以让是数字的字符串跟数字相加
'''
#print("1"+2) # 报错

# 字符串
print("\n\n"+"*"*15+"字符串"+"*"*15)
s = "Hello World"
s1 = 'Hello World'
s2 = '''Hello
		World'''
print(s,s1,s2)
print("*"*30)

# python 对字符串的访问支持正负索引
print(s[:])
print(s[1:]) # python 的所有索引起点都是0 区别于lua的从1开始的索引
print(s[1:3]) # 前闭后开区间
print(s[3:2]) # 无输出
print(s[-5:-2]) # 前闭后开区间 ->Wor
print("长度=",len(s)) # 查看字符串长度

print("字符串复制","*"*30)
print("字符串格式化","the first code is %s" % (s))
print("字符串成员运算符in,Hello 是否存在","Hello" in s)
print("字符串成员运算符not in,Hello 是否不存在","Hello" not in s)
print("原始字符串",r"Hello\n",R"World\n")
print("字符串全部转为大写字母",s.upper())
print("字符串全部转为小写字母",s.lower())
print("字符串查找",s.find("ll",1)) # 返回在字符串中的开始位置 找不到返回-1
#相比于find ，index方法找不到时会报错 还有从右边找的rfind rindex
#print("字符串查找",s.index("lle"))
print("字符串查找替换",s.replace("l","L",2)) # 最后一个参数是要替换的次数，不填，默认全部替换
print("字符串查找替换2",s.replace("l","L"))
#去除字符串左空格 lstrip ，右空格 rstrip,左右空格strip
ss = ["a","b","c"]
print("字符串以指定连接符连接","_".join(ss))
print("字符串以指定字符串分隔",s.split("l"))
print("字符串以换行符分隔",s2.splitlines(True)) # True 保留换行符 ,False 去掉换行符
print("字符串检查指定字符串重复出现次数",s.count("l"))
print("字符串开头检查",s.startswith("Hell"))
print("字符串结束检查",s.endswith("world"))
print("字符串只含数字检查",s.isdigit())
print("字符串只含字母检查",s.isalpha())
print("字符串只含数字或字母",s.isalnum())


# 列表 list python索引从0开始 
animal = ["cat","dog","fish","bird"]
for i in range(len(animal)):
	print(animal[i],end=",")
else:
	print()
print("*"*30)
# 不能越界，-5就报错 相对于lua，python对列表也提供负索引访问
for i in range(-4,len(animal)): 
	print(animal[i],end=",")
print()

#多维列表
arras = []
nums = 3
for i in range(nums):
	temp = []
	for j in range(nums):
		vi = i+1
		vj = j+1
		temp.append(vi*vj)
		#print("arras[%d][%d]=%d" % (vi,vj,vi*vj))
	arras.append(temp)
	
for i in range(nums):
	for j in range(nums):
		print("arras[%d][%d]=%d" % (i,j,arras[i][j]))

print("*"*30)
print(arras[0])
print(arras[0:2]) # python支持列表片段访问

arras[0][0] = 2
print("修改 arras[0][0] = ",arras[0][0])

del arras[0][0] # 删除序列中的元素
print("删除 arras[0][0] 后 arras[0]=",arras[0])

print("列表相加",[1,2,3]+[4,5,6])
print("列表相乘",["Hi"]*4)

# 元组 tuple 跟列表类似，但是不能修改元组中的数据 
print("元组",(1,2,3,"a",'b'))

# 字典
tab1 = {} # 申明一个空的字典跟列表一致
tab2 = {"x":1,"y":2,"z":"a",100:100} #-- 申明字典
print("字典",tab1)
#print(tab1["x"]) # tab1 中没有x，所以会报错
print(tab2["x"],tab2["z"]) # 访问字典table，索引不再是数字
tab1["x"] = 3
print("插入字典",tab1["x"])
del tab2["x"] # 删除元素
tab2[2] = 1
print(tab2)
# python中的键值必须是不可变的，可以是数字，字符串，元组


print("table.concat 连接")
print("table.insert 插入")
print("table.move 移动")
print("table.pack 封包")
print("table.remove 移除")
print("table.sort 排序")
print("table.unpack 解包")