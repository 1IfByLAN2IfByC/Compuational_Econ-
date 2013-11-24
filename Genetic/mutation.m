function f = mutation(pmut,clen,child)
tt = 1;
if (rand < pmut)
    idx = round(rand*(clen-1));
    tt = bitshift(tt,idx);
    temp = bitand(child,bitcmp(tt,clen));
    if(temp==child)
        child = child + tt;
    else
        child = temp;
    end
end
f = child;