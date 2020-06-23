function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

% Theta1 is 25x401                
                 
Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));
%Theta2 is 10x26 
                 
% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
% Theta1_grad is 25x401
Theta2_grad = zeros(size(Theta2));
% Theta2_grad is 10x26 

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
y_matrix = eye(num_labels)(y,:);
% create a 5000 by 10 matrix
% each row has a 1 in the col where the y vector gives the index
% e.g. if y row 2 had 5, then y_matrix row 2 will have 1 in the fifth column
A1 = [ones(m,1) X];
% add bias ones to X
% A1 is 5000x401 
Z2 = A1 * Theta1';
A2 = sigmoid(Z2); 
% A2 is 5000x25

A2 = [ones(size(A2,1),1) A2];
% add bias ones to A2, A2 now 5000x26
Z3 = A2 * Theta2';
A3 = sigmoid(Z3);
% A3 is 5000x10
h = A3;
% h and A3 are the same since this is the last output layer

J = (1/m) * (trace(-y_matrix' * log(h)) - trace((1-y_matrix)' * log(1-h)));
% trace gets the diagonal elements only from the matrix multiplication
% https://www.coursera.org/learn/machine-learning/discussions/all/threads/AzIrrO7wEeaV3gonaJwAFA
% since doing a matrix multiplication gets us more elements than we want to sum 
% really want only the y * log h term element wise 

% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%

D3 = A3 - y_matrix; %D3 is 5000 x 10 
D2 = (D3 * Theta2(:,2:end)) .* sigmoidGradient(Z2);
%remove the first column of bias units in Theta2, post removal is 10 x 25
% element wise multiply by sigmoidgraident (not sigmoid) of Z2
% D2 is 5000 x 25 since 5000x10 x 10x25 

Delta2 = D3' * A2;
% Triangle Delta2 is 10x26 since 10x5000 x 5000x26 

Delta1 = D2' * A1;
% Triangle Delta1 25x401 is since 25x5000 x 5000x401

Theta1_grad = (1/m)*Delta1; %25x401 
Theta2_grad = (1/m)*Delta2;  %10x26 

% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%
reg_theta1 = Theta1(:,2:end);
reg_theta2 = Theta2(:,2:end);
% want to temporarily remove the ones from theta matrices in order to do the regularization
% all rows, col 2 to end 

reg_sum_theta1 = trace(reg_theta1*reg_theta1');
reg_sum_theta2 = trace(reg_theta2*reg_theta2');

J = J + (lambda/(2*m)) * (reg_sum_theta1 +reg_sum_theta2);

Theta1(:,1) = 0; %still 25x401 
Theta2(:,1) = 0; %still 10x26 
% Sets 1st columns of Theta 1 and 2 to zero 

Theta1_grad = Theta1_grad + (lambda/m)*Theta1;
Theta2_grad = Theta2_grad + (lambda/m)*Theta2;
















% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
