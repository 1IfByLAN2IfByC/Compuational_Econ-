function genepool= initpopdet(popsize);
w = 2^21+2^16+2^13+2^8+2^5+2^0;
dec2bin(w,24)
genepool= w * ones(1,popsize);

