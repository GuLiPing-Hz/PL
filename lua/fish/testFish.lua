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
for i=1,10 do
    refresChair()
    print(string.rep("*",100))
end
