function [fit,bestind,bestfit] = fitness_gaportfol(pwm,mu,popsize,beta,sigma);
pret = pwm' * mu;
for j = 1:popsize;
    pvar(j) = 0.5 * beta * pwm(:,j)' * sigma * pwm(:,j);
end
fit = pret - pvar';
[top topi] = max(fit);
bestind = pwm(:,topi);
bestfit = top;

