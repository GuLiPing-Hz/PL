-- @ guliping

-- 协程 lua
-- 类似线程的概念

--还是最简单2个窗口卖票的行为

function sleep(second)
	if second > 0 then
		os.execute("ping -n " .. tonumber(second) .. " localhost > NUL") 
	end
end


local count = 1000 -- 1000的票

function sell(id)
	while(true) do
		if(count <= 0) then break end

		if(count == 50) then coroutine.yield() end
		print("count=",count,"I'm coroutine ",id)
		count = count - 1
	end
end

-- 创建协程
co1 = coroutine.create(sell)
co2 = coroutine.create(sell)

-- 唤起协程
print("main1", coroutine.resume(co1, 1))
print("main2", coroutine.resume(co2, 2))


while(count>0) do
	sleep(1)
end

print("main end")
