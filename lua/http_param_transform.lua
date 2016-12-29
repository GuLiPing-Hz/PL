function parse(s)
	local str = "map = "..s.." return map"
	local f = load(str)
	for k,v in pairs(f()) do
		print(k..":"..v)
	end
end	

parse("{uid=10327, os=1, ccode=86}")
