h = 1.00000001; % smaller won't halt in less than 1h.
x0 = 100000;
x = Busqueda(x0,h);
e = 1;
while e ~= 0
    prevX = x;
    x = Busqueda(prevX,h);
    e = x - prevX;
end
x
