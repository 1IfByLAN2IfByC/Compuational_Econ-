%Neighbor
function [temps, tempi, tempj] = neighbor(u,v,a_str,s,temps,tempi,tempj);

if (a_str(u,v).active == 0)

    if (s(u,v) >= temps)
        temps = s(u,v);
        tempi = u;
        tempj = v;
    end
    
end