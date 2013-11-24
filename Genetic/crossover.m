function [child0,child1] = crossover(clen,parent0,parent1);
crossov = round(rand*(clen-1));
maska=1;
for j = 1:(crossov-1)
    maska = bitshift(maska,1);
    maska = maska + 1;
end
child0 = bitor (bitand(parent0, maska), bitand(parent1, bitcmp(maska,clen)));
child1 = bitor (bitand(parent1, maska), bitand(parent0, bitcmp(maska,clen)));


