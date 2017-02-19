--[[
模块示例
]]

dA = {}

--定义模块变量
dA.a = 1

function dA.b()
	print("call dA.b()")
end

-- 模块私有函数
local function c()
	print("call c()")
end

--模块函数，调用模块私有函数
function dA.d()
	c()
end

--模块函数
dA.e = function()
	print("call e()")
end

return dA
