function genepool= initpoprand_gagame(popsize,clen);
for k1 = 1:popsize;
genepool(k1) = ceil(rand * (2^clen)-1);
%genepool(k1) =  (2^clen)-1;
dec2bin(genepool(k1), clen)
end
