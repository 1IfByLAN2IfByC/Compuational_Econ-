%Moveagent
function a_str = moveagent(a_str, s, i, j, temps, tempi, tempj); 

if (temps > s(i,j))
%Agent moves to best location and updates wealth
    a_str(tempi,tempj) = a_str(i,j);
    % Set old location to unoccupied
    a_str(i,j).active = 0; 
    a_str(i,j).vision = 0; 
    a_str(i,j).metabolism = 0; 
    a_str(i,j).wealth = 0;
    % Update wealth at new location
    a_str(tempi,tempj).wealth = a_str(tempi,tempj).wealth + temps - a_str(tempi,tempj).metabolism;
    % If wealth is less than zero set location to unoccupied
    if (a_str(tempi,tempj).wealth <= 0)
        a_str(tempi,tempj).active = 0; 
        a_str(tempi,tempj).vision = 0; 
        a_str(tempi,tempj).metabolism = 0; 
        a_str(tempi,tempj).wealth = 0;
    end
else
%Agent stays in position and updates wealth
    a_str(i,j).wealth = a_str(i,j).wealth + temps - a_str(i,j).metabolism;
    if (a_str(i,j).wealth <= 0)
        a_str(i,j).active = 0; 
        a_str(i,j).vision = 0; 
        a_str(i,j).metabolism = 0; 
        a_str(i,j).wealth = 0;
    end
end