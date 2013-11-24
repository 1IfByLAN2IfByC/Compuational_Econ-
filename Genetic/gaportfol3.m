%Genetic Algorithm portfolio program
%with initpoprand and parentsrand
%Program name: gaportfol3.m
% On early version by Hubert Salas

%initialization of counters and parameters;
nruns = 100;   popsize = 8; 

beta = 2;  
mu = [8 12 15]';
sigma = [6 -5  4;
        -5 17 -11;
         4 -11 24];

num = 3;   clen = num * 8;   pmut = 0.5;

%generation of chromosome strings of initial population
genepool= initpoprand_gaportfol(clen,popsize);
	
for k = 1:nruns;
	
	% transformation of crhomosome string into normalized n-asset portfolio
	pwm = normport(genepool,popsize,clen,num);
	
	% computation of fitness function and fittest individual
	[fit, bestind, bestfit] = fitness_gaportfol(pwm,mu,popsize,beta,sigma);
	wbest(:,k) = bestind;
    fbest(k) = bestfit;
	
	% selection of parents;
	parent0 = parentsrand(fit,popsize,genepool);
    parent1 = parentsrand(fit,popsize,genepool);
	
	% crossover of parentes chromosome strings
	[child0,child1] = crossover(clen,parent0,parent1);
	
	% mutation of children chromosome strings
    for h = 1:2:popsize;
	    child0mut = mutation(pmut,clen,child0);    
	    genenew(h) = child0mut;
	    child1mut = mutation(pmut,clen,child1);    
	    genenew(h+1) = child1mut;
	end
    genepool= genenew;
end

% print and graph optimal weights and criterion;
wbest
fbest
figure(1);
xaxis = [1:1:nruns]';
plot(xaxis,wbest(:,:));
figure(2);
xaxis = [1:1:nruns]';
plot(xaxis,fbest(:,:));