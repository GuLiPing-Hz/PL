'''

基础篇， 初识python
print 和 type都是 python内建的函数。
初识python类型和运算符

help函数可以给我们提供帮助文档

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

#多重赋值
a = b = c = 10
print(a,b,c)
a,b,c = 1,"a",2
print(a,b,c)


'''
python操作符

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

# 7.标识运算符
a = 1
b = 2
print("a is b =",a is b) #判断是否同一个对象
print("a is not b =",a is not b)
b = 1
print("a is b =",a is b)

