%Initsugarscape
%Initialize two-peak sugarscape and display
function s = initsugarscape(nruns, size, maxsugar);

%Generate sugarscape with one south west peak

x = -ceil(0.75*size) : size-ceil(0.75*size)-1; 
y = -ceil(0.25*size) : size-ceil(0.25*size)-1;

for i = 1:size;
    for j = 1:size;
        if (x(i) == 0 & y(j) == 0)
            s1(i,j) = maxsugar; 
        else
            s1(i,j) = maxsugar / (abs(x(i)) + abs(y(j)));
       end
    end
end

%Generate sugarscape with one north east peak
s2 = s1';

%Generate two-peak sugarscape
s = s1 + s2;

%Print maximum effective sugar level
maxrow = max(s);
max(maxrow)

%Display sugarscape
% figure(1);
% imagesc(s);
% axis square;
