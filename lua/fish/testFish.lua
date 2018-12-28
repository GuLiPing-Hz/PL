function tableToStr(tab,i)
    i = i or 0

    if i == 3 then
        return "table more than 3"
    else
        i = i + 1
    end
    if tab and type(tab) == "table" then
        local ret = ""
        for k,v in pairs(tab) do
            if type(k) ~= "number" or i == 1 then
                ret = ret.."tab["..k.."]=["..tableToStr(v,i).."];"
            else
                ret = ret.."["..tableToStr(v,i).."]"
            end
        end
        return "\n"..ret.."\n"
    else 
        return ""..tab
    end
end

function ConvertVersion(strVer)
    local n = 0
    local ver = 0
    string.gsub(
        strVer,
        '[^.]+',
        function(w)
            n = n + 1
            ver = ver * 65536 + tonumber(w)
        end
    )
    for i = n + 1, 4 do
        ver = ver * 65536
    end

    return ver
end

--print(ConvertVersion("1.2.2.1"))

function Split(str, reps)
    local resultStrList = {}
    string.gsub(str,'[^'..reps..']+',function ( w )
        table.insert(resultStrList, w)
    end)
    return resultStrList
end

function CompileVersion(verA,verB)
    if(verA == verB) then return 0 end

    local verAs = Split(verA,".")
    local verBs = Split(verB,".")

    local isVerANew = -1;
    local i = 1;
    while(i<=#verAs and i<=#verBs) do
        print(verAs[i],verBs[i])
        if (tonumber(verAs[i]) > tonumber(verBs[i])) then
            isVerANew = 1;
            break;
        end

        i = i+1
    end

    if(isVerANew ~= 1) then
        if(#verAs > #verBs) then
            return 1
        else
            return -1
        end
    else
        return 1
    end
end

-- print(CompileVersion("1.0.0.0","1.0.0"))
function getOrder()
    local order = { 1, 2, 3 }
    local AskRate = {10,30,60}
    local askOrder = {}
    for i = 1, 3 do
        sum = 0
        for i in ipairs(order) do
            sum = sum + AskRate[order[i]]
        end
        local rate = math.random(sum)
        -- print(rate)

        local start = 0
        local finish = 0
        for i in ipairs(order) do
            finish = start + AskRate[order[i]]
            if rate <= finish and rate > start then
                table.insert(askOrder, order[i]);
                table.remove(order, i)
                break
            end
            start = finish
        end
    end

    local str = ""
    for i,v in ipairs(askOrder) do str = str..","..v end
    print(str)
end

local __fish_rate_list = {
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6}}
function refresChair()
    for m = 1, #__fish_rate_list do
        local i, j, temp
        local l = #__fish_rate_list[m]
        for i = 1, l do
            j = math.random(l)
            temp = __fish_rate_list[m][i]
            __fish_rate_list[m][i] = __fish_rate_list[m][j]
            __fish_rate_list[m][j] = temp
        end
    end

    local str = ""
    for i,v in ipairs(__fish_rate_list) do 
        for j,v2 in ipairs(v) do
            str = str..","..v2
        end
        str = str .. "\n"
    end
    print(str)
end

math.randomseed(os.time())
-- for i=1,10 do
--     refresChair()
--     print(string.rep("*",100))
-- end

local DeskChairCnt = 4
function shuffle()
    local len, second = 6,10

    local desk_chair_rate_order = {}
    for i = 1, DeskChairCnt do --插入当前桌子的位置的一套鱼死亡轮询概率
        local rate_order = {}
        for i = 1, len do --先顺序插入位置
            table.insert(rate_order, i)
        end

        for i = 1, len * 2 do --随机调整位置
            local pos1 = math.random(len)
            local pos2 = math.random(len)
            rate_order[pos1], rate_order[pos2] = rate_order[pos2], rate_order[pos1]
        end
        table.insert(desk_chair_rate_order, rate_order)
    end

    print(tableToStr(desk_chair_rate_order))
    -- self.__fish_rate_total = len
    -- self.__fish_rate_per_sec = second
    -- self.__fish_rate_cur_index = 1
    -- self.__fish_rete_cur_sec = 0
    -- self.__fish_rate_list = desk_chair_rate_order
    -- for m = 1, #self.__fish_rate_list do
    --     local i, j
    --     local l = #self.__fish_rate_list[m]
    --     for i = 1, l do
    --         j = math.random(l)
    --         --交换位置
    --         self.__fish_rate_list[m][i],
    --             self.__fish_rate_list[m][j] = self.__fish_rate_list[m][j], self.__fish_rate_list[m][i]
    --     end
    -- end
end

shuffle()
shuffle()
shuffle()


function randOneList(list)
    local probs = list
    local total = 0
    for i = 1, #probs do
        total = total + probs[i]
        probs[i] = total
    end

    local r = math.random(total) --随机数
    for i = 1, #probs do
        if r <= probs[i] then
            return i
        end
    end
end

function randOne(...)
    local probs = table.pack(...)
    probs.n = nil
    return randOneList(probs)
end



print(randOne(100,200,300,400))
print(randOneList({100,200,300,400}))
