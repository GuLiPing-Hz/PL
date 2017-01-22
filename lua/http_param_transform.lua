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