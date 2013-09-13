function K = capital(n, theta, C)
    K = zeros(1, n);
    
    for i = 1:n 
        K(i) = K(i-1) + theta* K(i-1) - C(i); 
        