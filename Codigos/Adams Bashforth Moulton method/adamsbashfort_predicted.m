function [y, td] = adamsbashfort_predicted(f, alpha, y0, T, N, tol, n_max)
    % Variable for running program
    h = T/N;
    td = 0:h:T;
    m = ceil(alpha);
    len_vars = length(alpha);
    
    ks = 1:N;
    k = repmat(ks, len_vars, 1);
    
    % Calculating a and b
    b = k.^alpha - (k-1).^alpha;
    a = (k+1).^(alpha+1) - 2*(k.^(alpha+1)) + (k-1).^(alpha + 1);
    
    y = zeros(len_vars,N+1);
    fs = zeros(len_vars, N+1);
    
    y(:,1) = y0;
    f0 = f(y0);
    fs(:, 1) = f0;
    
    k1 = 0:m-1;
    fact = factorial(k1);
    term1 = (h.^alpha)./gamma(alpha + 1); 
    term2 = term1./(alpha + 1);
    
    for j=1:N
        % Calculating predicted value
        aux = ((j*h).^k1).*y0./fact;
        aux = sum(aux, 2);
        
        k2 = ks(1:j);
        fs(:, j) = f(y(:, j));
        
        fv = fs(:, 1:j);
        sum2 = sum(b(:, j+1-k2).*fv, 2);        
        p = aux + term1.*sum2;
        
        % Calculating next y
        sum3 = sum(a(:, j+1-k2).*fv, 2);
        
        i = 0;
        pant = p - tol - 1;
        term3 = ((j-1).^(alpha+1) - (j-1-alpha).*j.^alpha).*f0;
        while norm(p - pant) > tol || i < n_max
            pant = p;
            
            % Calculating next p
            p_initial = f(pant) + term3;
            p = aux + term2.*(p_initial + sum3);    
            i = i + 1;
        end
        
        y(:, j+1) = p;
    end
    
end

