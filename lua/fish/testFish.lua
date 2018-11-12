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

print(CompileVersion("1.0.0.0","1.0.0"))
