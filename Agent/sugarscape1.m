%Sugarscape1
%sugarscape: (two-peak sugarscape, rule: Ginf)
%agents: (moving sequence: random, view: four directions, rule: M)

%Initialize model parameters
nruns = 6; 
size = 50; %even number
metabolismv = 4;
visionv = 6; %set always smaller than size
maxsugar = 20;

%Initialize sugarscape and display 
s = initsugarscape(nruns, size, maxsugar);

%Initialize agents population 
a_str = initagents(size, s, visionv, metabolismv);


%Main loop (runs)
for runs = 1:nruns;

    %Display agents locations 
	dispagentloc(a_str, size, nruns, runs);
    
	%Select agents in a random order and move around the sugarscape following rule M
    for i = randperm(size); 
        for j = randperm(size);
             
            if (a_str(i,j).active == 1) %is there an angent on this location?
  
                %Agent explores sugarscape in random directions and selects best location
                temps = s(i,j);  
                tempi = i;  
                tempj = j;
               
                for k = a_str(i,j).vision : -1 : 1;  
                    [temps, tempi, tempj] = see(i,j,k,a_str,s,size,temps,tempi,tempj);                 
                end
                
                %Agent moves to best location, updates sugar stock and eats sugar
                a_str = moveagent(a_str, s, i, j, temps, tempi, tempj);                 
            end       % if 
            
        end           % for j
    end               % for i
    
end                   % for runs