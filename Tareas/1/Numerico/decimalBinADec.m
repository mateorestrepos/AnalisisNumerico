format long

x = '0.110011001100110011001100';
y = '110101110';
z = '11111.11111';

b = bina2deca(x);
err = 0.8 - b;
eps = err/0.8;
