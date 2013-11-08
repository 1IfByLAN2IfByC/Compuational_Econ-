%Sugarscape1
%sugarscape: (two-peak sugarscape, rule: Ginf)
%agents: (moving sequence: random, view: four directions, rule: M)

%Initialize model parameters
nruns = 6; 
size = 50; %even number
metabolismv = 5;
visionv = 7; %set always smaller than size
maxsugar = 20;
regenrate = 2;
depleterate = 2; % larger => slower depletion
deadzones = zeros(1, nruns);

%Initialize sugarscape and display 
s = initsugarscape(nruns, size, maxsugar);

%Initialize agents population 
a_str = initagents(size, s, visionv, metabolismv);


%Main loop (runs)
for runs = 1:nruns;

    %Display agents locations 
	current_loc = dispagentloc(a_str, size, nruns, runs);
    
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
    
    % update the new sugarscape after depletion and regeneration effects
    s = metab(a_str, s, regenrate, depleterate, nruns, runs);
    
    deadzones(1,runs) = sum(s(:) <= 0 );
    
end                   % for runs