% See
function [temps, tempi, tempj] = see(i,j,k,a_str,s,size,temps,tempi,tempj);

south = [i+k  size  i+k-size  j  i+k  j];
north = [k-i  -1  i-k+size  j  i-k  j];
east  = [j+k  size  i  j+k-size  i  j+k];
west  = [k-j  -1  i  j-k+size  i  j-k];

c{1} = south;  c{2} = north;  c{3} = east;  c{4} = west;

for m = randperm(4);

	if (c{m}(1) > c{m}(2))
        u = c{m}(3);
        v = c{m}(4);
        [temps, tempi, tempj] = neighbor(u,v,a_str,s,temps,tempi,tempj);   
	else    
        u = c{m}(5);
        v = c{m}(6);
        [temps, tempi, tempj] = neighbor(u,v,a_str,s,temps,tempi,tempj);     
	end
    
end