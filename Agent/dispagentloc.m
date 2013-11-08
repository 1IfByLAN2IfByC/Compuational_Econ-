%Dispagentloc
%Transform field "agent" from data structure into matrix and display agents locations    
 function  a = dispagentloc(a_str, size, nruns, runs);
a = zeros(size); av = zeros(size); am = zeros(size);

for i = 1:size;
    for j = 1:size;
        if (a_str(i,j).active == 1)
	        a(i,j) = a_str(i,j).active;
            av(i,j) = a_str(i,j).vision;
            am(i,j) = a_str(i,j).metabolism;
        end
    end
end

figure(2);
subplot(ceil(sqrt(nruns)),ceil(sqrt(nruns)) - 1,runs), spy(a);
axis square
title('Agent Location')

avgvision = sum(sum(av))/sum(sum(a))
avgmetabolism = sum(sum(am))/sum(sum(a))
