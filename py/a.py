'''

基础篇， 初识python
print 和 type都是 python内建的函数。
初识python类型

http://blog.csdn.net/glp3329/article/details/52511855
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

'''作死除法
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
'''
#0/0

