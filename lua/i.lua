-- @ guliping

-- 协程 lua
-- 类似线程的概念

--看懂下面例子的输出就能理解lua的协程，lua的协程同一时刻只能运行一个
function foo (a)
	print("foo",coroutine.running())
	print("foo", a)
	return coroutine.yield(2*a)--这里挂起子线程，并将yield中的值当做coroutine.resume的返回值
end

--这里创建一个协程，指定需要传入两个参数
co = coroutine.create(function (a,b)
	print("co-body",coroutine.running())--当前不是主线程
	print("coroutine status",coroutine.status(co))
	print("co-body", a, b)
	local r = foo(a+1)--调用外部函数
	print("co-body", r)
	local r, s = coroutine.yield(a+b, a-b)--挂起子线程，并把算出来的两个值返回
	print("co-body", r, s)
	return b, "end"--函数执行结束，返回最后的值
end)

print("main",coroutine.running())--返回当前的线程对象，和一个是否是主线程的bool值
print("main coroutinen status=",coroutine.status(co))--返回coroutine的当前状态
--"suspended" "running" "dead"

--1和10会传入coroutine.create创建的函数，主线程挂起
print("main", coroutine.resume(co, 1, 10))
--如果子线程没有报错，coroutine.resume默认第一参数是true 后面才是yield返回的参数

print("main",coroutine.running())
print("main coroutine status=",coroutine.status(co))

--这里直接回到子线程刚才yield的位置继续执行，并且把"rrr"当做子线程中
--coroutine.yield的返回值，所以上面foo返回的其实是这里传入的值
print("main", coroutine.resume(co, "rrr"))
print("main", coroutine.resume(co, "x", "y"))--这里同样的道理传入"x","y"

print("main coroutinen status=",coroutine.status(co))
print("main", coroutine.resume(co, "x", "y"))--已经死掉的线程无法再resume了
