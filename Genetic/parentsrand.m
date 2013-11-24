function f = parentsrand(fit,popsize,genepool);
cumfit = sum(fit);
val = 0;
spin_val = rand * cumfit;
j = 1;
while ((val < spin_val) & (j < popsize))
    val = val + fit(j);
    j = j + 1;
end
f = genepool(j);
