function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%
% X = [ones(m, 1) X]; %don't need this step since ex5 does it in the input. adding ones to X, now 12x2
h = X * theta; % h is 12x1 
J = 1/(2*m) * ((h - y)' * (h - y)) ; %element wise squaring of hx - y

theta(1) = 0 ;
reg_err = (lambda / (2*m)) * (theta' * theta); %regularisation term
J = J + reg_err; % update J with regularised

grad = (1/m)* X' * (h - y); 
% 2x12 * 12x1 becomes 2x1 + 2x1 
reg_err_grad = (lambda/m) * theta;
grad = grad + reg_err_grad; % update grad with regularised 











% =========================================================================

grad = grad(:);

end
