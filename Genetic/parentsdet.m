function [parent0,parent1] = parentsdet(fit,genepool); 
[top topi] = max(fit);
parent0 = genepool(topi);
fit(topi) = 0;
[top topi] = max(fit);
parent1 = genepool(topi);
