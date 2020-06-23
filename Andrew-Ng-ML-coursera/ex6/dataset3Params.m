function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

C_values = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
sigma_values = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
% setup list of C and sigma values we want to test for 

results_matrix = zeros(length(C_values) * length(sigma_values), 3);
% setup matrix for each C_val, sigma_val, error combination. X by 3 matrix   

row = 1; 
for C_val = C_values
  for sigma_val = sigma_values


    model = svmTrain(X, y, C_val, @(x1, x2) gaussianKernel(x1, x2, sigma_val)); 
    % train on C_val and sigma_val 
    predictions = svmPredict(model, Xval);
    prediction_err = mean(double(predictions ~= yval)); 

    results_matrix(row,:) = [C_val sigma_val prediction_err];
    % store each loop's iteration on a row in the matrix
    row = row + 1; 
  endfor;
endfor;

[min_values, indices] = min(results_matrix, [], 1);
% get the min values and the index of those values from the results matrix 
min_row = results_matrix(indices(3),:);
% based on the min prediction error in column 3 of indices, pull the row from results_matrix
C = min_row(1);
sigma = min_row(2);

% =========================================================================

end
