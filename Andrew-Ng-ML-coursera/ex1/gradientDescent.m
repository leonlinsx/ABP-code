function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESCENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCost) and gradient here.
    %
    %temp1 = theta(1) - alpha * (1/m) * sum((X*theta - y));
    %theta(1) = theta(1) - (alpha * (1/m)) * sum((X*theta - y) .* X(:,2));
    %take the first row of theta, and the sum of the matrix formed from X * theta - y, 
    %and for theta(2), multiply by the 2nd column of X, since X was created with additional column 
   
    
    h = X * theta;
    errors_vect = h - y;
    theta_change = alpha * (1/m) * (X' * errors_vect);
    theta = theta - theta_change; 
    


    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);

end

end
