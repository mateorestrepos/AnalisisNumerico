function x = euler(f,h,T,x0)
    N = ceil(T/h);
    x = zeros(length(x0), N);
    x(:,1) = x0;
    for k=2:N
        x(:,k) = x(:,k-1) + h*f(x(:,k-1))';
    end
end

