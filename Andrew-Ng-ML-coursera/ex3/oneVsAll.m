function [all_theta] = oneVsAll(X, y, num_labels, lambda)
%ONEVSALL trains multiple logistic regression classifiers and returns all
%the classifiers in a matrix all_theta, where the i-th row of all_theta 
%corresponds to the classifier for label i
%   [all_theta] = ONEVSALL(X, y, num_labels, lambda) trains num_labels
%   logistic regression classifiers and returns each of these classifiers
%   in a matrix all_theta, where the i-th row of all_theta corresponds 
%   to the classifier for label i

% Some useful variables
m = size(X, 1);
n = size(X, 2);

% You need to return the following variables correctly 
all_theta = zeros(num_labels, n + 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the following code to train num_labels
%               logistic regression classifiers with regularization
%               parameter lambda. 
%
% Hint: theta(:) will return a column vector.
%
% Hint: You can use y == c to obtain a vector of 1's and 0's that tell you
%       whether the ground truth is true/false for this class.
%
% Note: For this assignment, we recommend using fmincg to optimize the cost
%       function. It is okay to use a for-loop (for c = 1:num_labels) to
%       loop over the different classes.
%
%       fmincg works similarly to fminunc, but is more efficient when we
%       are dealing with large number of parameters.
%
% Example Code for fmincg:
%
%     % Set Initial theta
%     initial_theta = zeros(n + 1, 1);
%     
%     % Set options for fminunc
%     options = optimset('GradObj', 'on', 'MaxIter', 50);
% 
%     % Run fmincg to obtain the optimal theta
%     % This function will return theta and the cost 
%     [theta] = ...
%         fmincg (@(t)(lrCostFunction(t, X, (y == c), lambda)), ...
%                 initial_theta, options);
%
initial_theta = zeros(n+1,1);

options = optimset('GradObj','on','MaxIter',50);

for c = 1:num_labels
  [theta] = fmincg(@(t)(lrCostFunction(t, X, (y==c), lambda)), initial_theta, options);
  all_theta(c,:) = theta';
% y==c returns 1 only when in that num_label for that iteration of the loop
% so only those row elements in X that match the num_label are returned
% i.e. y is either 0 or 1 after y==c, and that determines whether it's in class (1) or not (0)
% and whether those X elements in that row return the number for the num_label 

  
% each iteration of the loop a theta is optimised for that number (0 to 9)
% need to store this in the all_theta matrix that is num_labels by n+1, so we get a theta for every num_label (0 to 9)  
% using all the columns of row c in all_theta, pass in theta transpose   
endfor 







% =========================================================================


end
