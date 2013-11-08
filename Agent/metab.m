function s = metab(struct, scape, regenRate, depleteRate, nruns, runs)

    y = zeros(length(scape),length(scape));
    rates = zeros(length(scape),length(scape));
    
    
    % first find the 2D convolution matrix of each cell to find
    % depletion/regen rates 
    
    for i = [1:length(scape)]
        
        for j = [1:length(scape)]
            
            rates(i,j) = struct(i,j).metabolism;
            
   
    
        end
    end
    
     rates = conv2(rates, [1 1 1;1 0 1;1 1 1],'same'); 
    
    
   
    for i = [1:length(scape)]
        
        for j = [1:length(scape)]
            
            if struct(i,j).active ~= 0 && rates(i,j) ~= 0 
                % if the cell is active, then the sugarscape is depleted
                y(i,j) = - round(rates(i,j) / depleteRate) + 1; 
                
            elseif struct(i,j).active == 0 && rates(i,j) ~= 0
                % if no one is there, but someone is near
                y(i,j) = round(regenRate / rates(i,j)) + 1 ;
                
                
            else
                % if no one is there and no one is around
                y(i,j) = regenRate + 1;
                
                
            end    %if
            
        end     %j
        
    end     %i
    
    % update the sugarscape based on above depelation rates
    s = scape + y; 
    
    [X,Y] = meshgrid([1:length(scape)], [1:length(scape)]);

    figure(3)
    subplot(ceil(sqrt(nruns)),ceil(sqrt(nruns)) -1 ,runs), imagesc(y)
    title('Net Regeneration')
    colorbar
    
    figure(1)
    subplot(ceil(sqrt(nruns)),ceil(sqrt(nruns)) -1 ,runs), imagesc(scape)
    title('Sugarscape')
    colorbar
    
    
            
                
                
                
                