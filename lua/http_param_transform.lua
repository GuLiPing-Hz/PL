-- lua 5.3.2
--@ guliping

function parse(s)
	local str = "map = "..s.." return map"
	local f = load(str)
	for k,v in pairs(f()) do
		print(k..":"..v)
	end
end	

--调用的时候务必把参数中的中文改成英文或数字
parse("{gid=248957, uid=110457, lid=100000, os=1, tid=7474412, ccode=86}")

--URL = http://api.sociapoker.com/league/getSettlementInfo;
--Param={gid=248957, uid=110457, lid=100000, os=1, tid=7474412, ccode=86}

-- python 接口返回中文数据，转换成中文
function show_utf8(s)
	local temp = string.gsub(s,"\\u","0x")
	if(#temp % 6 ~= 0) then
		print("Error Str")
		return
	end

	local utf8s = ""
	local pos = 0
	while pos < #temp do
		local start = string.find(temp,"0x",pos)
		local ed = start + 6
		pos = ed
		local c = string.sub(temp,start,ed-1)
		-- print(c)
		local c_num = tonumber(string.sub(c,3),16)
		-- print(c_num)
		utf8s = utf8s..utf8.char(c_num)
		
	end
	print("接口返回utf8字符转中文:"..s.." ->"..utf8s)
	-- print(utf8.len(temp))
	-- print(utf8.char(0x7248))
end

show_utf8("\\u7248\\u672c\\u8fc7\\u4f4e\\uff0c\\u8bf7\\u5347\\u7ea7\\uff01")
