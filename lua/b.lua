#!lua 5.3.2

--[[

lua 变量
lua中的变量有三种类型，全局变量，局部变量，表域
lua 中的变量全是全局变量，那怕是语句块或是函数里，除非用 local 显示声明为局部变量
局部变量的作用域为从声明位置开始到所在语句块结束。
变量的默认值均为 nil

应该尽可能的使用局部变量，有两个好处：
1. 避免命名冲突。
2. 访问局部变量的速度比全局变量更快。
--]]

a = 5               -- 全局变量
local b = 5         -- 局部变量

function joke()
    c = 5           -- 全局变量
    local d = 6     -- 局部变量
end

joke()
print(c,d)          --> 5 nil

do 
    local a = 6     -- 局部变量
    b = 6           -- 全局变量
    print(a,b);     --> 6 6
end

print(a,b)      --> 5 6


--[[ 
Lua可以对多个变量同时赋值，变量列表和值列表的各个元素用逗号分开
，赋值语句右边的值会依次赋给左边的变量。
--]]

--[[
遇到赋值语句Lua会先计算右边所有的值然后再执行赋值操作，所以我们可以这样进行交换变量的值：
]]

x = 1
y = 2
print("x=",x,";y=",y)
x,y = y,x
print("x=",x,";y=",y)

--[[
当变量个数和值的个数不一致时，Lua会一直以变量个数为基础采取以下策略：
a. 变量个数 > 值的个数             按变量个数补足nil
b. 变量个数 < 值的个数             多余的值会被忽略
--]]

--table 的索引访问有三个方法，使用[],或者点，或者内建函数
tab = {}
tab["n"] = 10
print("tab.n=",tab.n)
print("tab.n=",rawget(tab,"n"))

--[[
流程控制
--]]
if true then
	print("is true")
end

a = 1
if a == 0 then
	print("a=0")
elseif a == 1 then
	print("a=1")
else
	print("a~=0")
end

--[[
循环
--]]
n = 5
while(n > 0) do
	print("n=",n)
	n = n-1
end

print("*********************************")

-- 数值for循环
n = 6
for i=1,n do -- for中的表达式在开始循环前只计算一次
	print("i=",i)
end

for i=6,0,-2 do -- 循环初始化，指定结束值，指定步长
	print("i=",i)
end

-- 泛型for循环
for k,v in pairs(_G) do --查看当前lua环境中已经定义的function，table
	print(k,v)
end

tab = {10,9,8,7,6}
for i,v in ipairs(tab) do
	print(i,v)
end

r = 5
repeat
	print("r=",r)
	r = r+1 -- r++ r+=1 错误
	break -- 跳出循环
until(r >= 9)
