--[[

基础篇， 初识lua
print 和 type都是 lua内建的函数。
初识lua类型和运算符

http://blog.csdn.net/glp3329/article/details/52511855
--]]

--[[
    lua多行注释
--]] --这里习惯在前面加上'--'
print(type(a)) -- 输出 nil
a = "123"
print(type(a)) -- 输出 string
a = 12
print(type(a)) -- 输出 number
a = 12.3
print(type(a)) -- 输出 number
print(0/0) -- 输出 nan  意思就是Not a Number 不是数字
print(type(0/0)) -- 输出 number , 意思就是nan都是number

--多重赋值
-- a = b = c = 10 不允许连等
print(a,b,c) -- 未定义的变量默认值是nil
a,b,c = 1,"a",2
print(a,b,c)


--[[
python操作符

在交互模式下，python会把运算的结果保存在 '_' 里面
--]]

-- 1.算术运算符:
a = 10
b = 20
print("a+b=",a+b) --加
print("a-b=",a-b) --减
print("a*b=",a*b) --乘
print("b/a=",b/a) --除
print("b%a=",b%a) --模
print("b^a=",b^a) --指数  lua使用这个当指数，意味着不能把它当按位异或运算了，我们有其他方法
print("b//a=",b//a) --地板除 取整
print("-a=",-a)
print("*********************************")

-- 2.比较操作符:
print("a==b",a==b)
print("a~=b",a~=b) -- 这个区别与别的 !=
print("a>b",a>b)
print("a<b",a<b)
print("a>=b",a>=b)
print("a<=b",a<=b)

--a += 2 lua中没有这样的赋值运算符，需要自己写成 a = a+2

-- 3.逻辑运算符:
a = true -- 这里必须小写
b = false
print(a and b) 	--等价与 &&
print(a or b) 	--等价与 ||
print(not a) 	--等价与 !

-- 4.其他运算符

--字符串连接符 ..
a = "123"
b = "abc"
print(a..b)

--长度计算符 #
print(#a) -- 计算字符串长度
b = {1,2}
print(#b) -- 计算table size

