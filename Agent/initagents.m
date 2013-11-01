%Initagentsage
%Initialize agents population including age range
function a_str = initagentsage(size, s, visionv, metabolismv);
for i = 1:size;
    for j = 1:size;
        
        if (rand < 0.2)
            a_str(i,j).active = 1; %put an agent on this location
            a_str(i,j).metabolism = ceil(rand * metabolismv);
            a_str(i,j).vision = ceil(rand * visionv);
            a_str(i,j).wealth = s(i,j); 
            
        else
            a_str(i,j).active = 0; %keep this location empty
            a_str(i,j).metabolism = 0;
            a_str(i,j).vision = 0;
            a_str(i,j).wealth = 0;    
            
        end
    end
end

