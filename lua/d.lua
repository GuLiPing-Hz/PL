#!lua 5.3.2
--[[
lua 数据类型详解
--]]

-- 字符串
print("\n\n"..string.rep("*",15).."字符串"..string.rep("*",15))
s = "Hello World"
s1 = 'Hello World'
s2 = [[Hello
		World]]
print(s,s1,s2)
print(string.rep("*",30))--"*********************************")

-- lua 对字符串的访问支持正负索引
print(string.sub(s,0))
print(string.sub(s,1)) -- lua 的所有索引起点都是1 区别于其他的从0开始的索引
print(string.sub(s,1,3)) -- 前后闭区间
print(string.sub(s,3,2)) -- 无输出
print(string.sub(s,-5,-2)) -- 前后闭区间 ->Worl
print("长度=",#s,string.len(s)) -- 查看字符串长度

print("字符串复制",string.rep("*",30))
print("字符串格式化",string.format("the first code is %s",s)) -- 格式等价于C语言
print("字符串全部转为大写字母",string.upper(s))
print("字符串全部转为小写字母",string.lower(s))
print("字符串查找",string.find(s,"ll",1)) -- 返回在字符串中的开始位置和结束位置，找不到返回nil
print("字符串查找替换",string.gsub(s,"l","L",2)) -- 最后一个参数是要替换的次数，不填，默认全部替换
print("字符串查找替换2",string.gsub(s,"l","L"))
print("字符串反转",string.reverse(s))
-- char是把数字转换成字符串，byte把字符串转换成数字
print("字符串ASII码",string.char(0),string.char(97),string.byte(s,2))


-- 列表（数组 table） lua索引从1开始

animal = {"cat","dog","fish","bird"}
for i=1,#animal do print(animal[i]) end
print(string.rep("*",30))
--for k,v in pairs(animal) do print(v) end
-- lua对列表不提供负索引访问
for i=-5,#animal do print(animal[i]) end -- 未定义的输出nil

--多维数组
arras = {}
nums = 3
for i=1,nums do
	arras[i] = {}
	for j=1,nums do
		arras[i][j] = i*j
		--print(string.format("arras[%d][%d]=%d",i,j,arras[i][j]))
	end
end

for i=1,nums do
	for j=1,nums do
		print(string.format("arras[%d][%d]=%d",i,j,arras[i][j]))
	end
end
print(string.rep("*",30))
print(arras[1])

arras[1][1] = 2
print("修改 arras[1][1] = ",arras[1][1])

arras[1][1] = nil -- 删除数组中的元素
print("删除 arras[1][1] 后 arras[1]=",arras[1])

--print("列表相加",{1,2,3}+{4,5,6}) --不支持需要自己重载
--print("列表相乘",{"Hi"}*4)

-- 字典 （table） lua中所有的数据结构都可以通过table实现
tab1 = {} -- 申明一个空的字典跟列表一致
tab2 = {x=1,y=2,z="a",100} -- 申明字典
print("字典",tab1)
print(tab1.x,tab2.x,tab2["z"]) -- 访问字典table，索引不再是数字
tab1.x = 3
print("插入字典",tab1.x)
tab2.x = nil -- 删除元素
tab2[2] = 1
print(tab2)
-- lua 中申明table的时候无法指定数字作为(key=vale)中的key，但是可以给单独的值，


print("table.concat 连接")
print("table.insert 插入")
print("table.move 移动")
print("table.pack 封包")
print("table.remove 移除")
print("table.sort 排序")
print("table.unpack 解包")


-- 迭代器
-- lua的迭代器是由函数构成，简单举个例子:
function my_itera(arra)
	arra = arra or {}
	local index = 0
	local size = #arra
	return function() -- 闭包内函数，可以访问闭包内的变量
		index = index + 1
		if(index <= size) then
			return arra[index]
		end
	end
end

tab = {1,2,3}
for v in my_itera(tab) do
	print(v)
end

-- 不过感觉lua内建的 ipairs 和 pairs 已经够用了
