function pwm = normport(genepool,popsize,clen,num);
genetemp = genepool;
for i = 1:popsize;
n=ceil(clen/num);
mask = 2^n-1;
port = zeros(1,num);
    for j = 1:num
        port(num-j+1) = bitand(genetemp(i),mask);
        genetemp(i)=bitshift(genetemp(i),-n);
    end
port = port/sum(port);
pwm(:,i) = port'; 
end