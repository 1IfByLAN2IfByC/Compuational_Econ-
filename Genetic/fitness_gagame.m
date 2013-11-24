function [fit,bestind,bestfit] = fitness_gagame(genepool,popsize,clen);

payoffs(1,popsize) = 0;

% Loop for player1 
for k1 = 1:popsize;
    strategyp1 = genepool(k1);
   
    % Loop for opponents (player2)
    for k2 = 1:popsize;
    strategyp2 = genepool(k2);
    
        if (k1 ~= k2)
            mask = 1;
            
            %Loop for games
            for k3 = 1:clen;    
            actionp1 = bitand(strategyp1,mask);
            actionp2 = bitand(strategyp2,mask);
            mask = bitshift(mask,1);
                % defect, defect
                if (actionp1 == 0) & (actionp2 == 0)
                    payoffs(k1) = payoffs(k1) + 1;
                end
                % cooperate, defect
                if (actionp1 > 0) & (actionp2 == 0)
                    payoffs(k1) = payoffs(k1) + 0;
                end
                % defect, cooperate
                if (actionp1 == 0) & (actionp2 > 0)
                    payoffs(k1) = payoffs(k1) + 5;
                end
                % cooperate, cooperate
                if (actionp1 > 0) & (actionp2 > 0)
                    payoffs(k1) = payoffs(k1) + 3;
                end
            end % end loop games
            
        end % end if
        
    end % end loop opponents

end % end loop player1

fit = payoffs;
[top topi] = max(fit);
bestind = genepool(topi);
bestfit = top;
