a = 0;
b = 0.1;

for n=1:10000
    l0 = (a + b)/2;
    l1 = (a + l0)/2;
    
    sum1 = 1 + l1;
    if sum1 == 1
        a = l1;
    else
        b = l1;
    end
end

pr = ['The epsilon of the computer is ' num2str(l1)];
disp(pr);