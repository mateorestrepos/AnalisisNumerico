function dec = bina2deca(bin)
    exponent = find(bin, 'e');
    
    arbin = bin - '0';
    point = find(arbin, -2);
    
    if ~isempty(point)
        ent = arbin(1:point-1);
        deci = arbin(point+1:length(arbin));
    else
        ent = arbin;
        deci = 0;
    end 
    
    ent2 = zeros(1,length(ent));
    for i=1:length(ent2)
        ent2(i) = 2^(length(ent2) - i);
    end
    entdec = sum(ent2.*ent);
    
    dec2 = zeros(1,length(deci));
    for j=1:length(dec2)
        dec2(j) = 2^(-j);
    end
    dec3= sum(dec2.*deci);
    
    dec = entdec + dec3;
    
end

