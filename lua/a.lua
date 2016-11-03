--[[

基础篇， 初识lua
print 和 type都是 lua内建的函数。
初识lua类型

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

