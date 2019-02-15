function [max] = Busqueda(x0,h)
    num = x0;
    i = 1;
    while num < Inf
        numPrev = num;
        num = num*h;
    end
    max = numPrev;
end

