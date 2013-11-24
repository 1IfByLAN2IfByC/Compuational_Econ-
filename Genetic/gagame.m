% Genetic Algorithm evolutionary game program
% with initpopdet and parentsdet
% Program name: gagame.m
% On an early version by Huber Salas

% initialization of counters and parameters;
nruns = 100;   popsize = 8; 

clen = 24;   pmut = 0.5;

% generation of chromosome strings of initial population
genepool= initpoprand_gagame(popsize,clen);
	
for k = 1:nruns;
	
	% computation of fitness function and fittest individual
	[fit, bestind, bestfit] = fitness_gagame(genepool,popsize,clen);
	wbest(k) = bestind;
    fbest(k) = bestfit;
	
	% selection of parents;
	[parent0,parent1] = parentsdet(fit,genepool);
	
	% crossover of parents chromosome strings
	[child0,child1] = crossover(clen,parent0,parent1);
	
	% mutation of children chromosome strings
	for h = 1:2:popsize;
	    child0mut = mutation(pmut,clen,child0);    
	    genenew(h) = child0mut;
	    child1mut = mutation(pmut,clen,child1);    
	    genenew(h+1) = child1mut;
	end
    genepool = genenew;
end

% print and graph fittest individual;
dec2bin(wbest(nruns),clen)
fbest = fbest / (clen * (popsize - 1));
figure(1);
xaxis = [1:1:nruns]';
plot(xaxis,wbest);
figure(2);
xaxis = [1:1:nruns]';
plot(xaxis,fbest);
