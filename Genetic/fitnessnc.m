function [fit,bestind,bestfit] = fitnessnc(pwm,mu,popsize,beta,sigma,num);

% Portfolio Redistribution 
for j = 1:popsize;
    cond = ones(num,popsize);
    counter = num;
    acum = 0;
    
    for i = 1:num;
        if pwm(i,j) < 0.1
            acum = acum + pwm(i,j);
            pwm(i,j) = 0;
            cond(i,j) = 0;
            counter = counter - 1;
        end
    end
    
    for i = 1:num;
        if counter > 0
            if cond(i,j) == 1;
                pwm(i,j) = pwm(i,j) + (acum / counter);
            end
        end
    end
    
end

% Computation of portfolio returns and best portfolio
fc = 0.2 * ones(1,num);
mc = 0.05 * ones(1,num);
pret = pwm' * mu;
for j = 1:popsize;
    pvar(j) = 0.5 * beta * pwm(:,j)' * sigma * pwm(:,j);
end
for j = 1:popsize;
    pbrok(j) = fc * cond(:,j) + mc * pwm(:,j);
end
fit = pret - pvar' - pbrok';
[top topi] = max(fit);
bestind = pwm(:,topi);
bestfit = top;

