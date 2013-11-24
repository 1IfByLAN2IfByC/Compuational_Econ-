function genepool= initpoprand_gaportfol(clen,popsize); 
mask = 1;
genepool= zeros(1,popsize);
for j = 1:popsize
    for i = 1:clen
        if (rand < 0.5)
            genepool(j) = bitor(genepool(j),mask);
        end
        genepool(j) = bitshift(genepool(j),1);
    end
    genepool(j) = bitshift(genepool(j),-1);
end