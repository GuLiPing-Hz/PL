#!lua 5.3.2

--[[ 使用模块 
http://blog.csdn.net/glp3329/article/details/52538511
]]

local dA = require "dA" --后缀名默认  .lua

print(dA)
print("模块内容")
for k,v in pairs(dA) do print(k,v) end

dA.d()
dA.e()



'''
require 用于搜索 Lua 文件的路径是存放在全局变量 package.path 中，
当 Lua 启动后，会以环境变量 LUA_PATH 的值来初始这个环境变量。
如果没有找到该环境变量，则使用一个编译时定义的默认路径来初始化。
当然，如果没有 LUA_PATH 这个环境变量，也可以自定义设置，
在当前用户根目录下打开 .profile 文件（没有则创建，打开 .bashrc 文件也可以），
例如把 "~/lua/" 路径加入 LUA_PATH 环境变量里：
'''

--require 引用路径
print(package.path)

--如果找到该文件，那么使用package.loadfile加载文件，
--否则搜索package.cpath的so或者dll文件，通过package.loadlib加载


--C/C++封装的模块