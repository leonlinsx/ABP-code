function idx = findClosestCentroids(X, centroids)
%FINDCLOSESTCENTROIDS computes the centroid memberships for every example
%   idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
%   in idx for a dataset X where each row is a single example. idx = m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
%

% Set K
K = size(centroids, 1);

% You need to return the following variables correctly.
idx = zeros(size(X,1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Go over every example, find its closest centroid, and store
%               the index inside idx at the appropriate location.
%               Concretely, idx(i) should contain the index of the centroid
%               closest to example i. Hence, it should be a value in the 
%               range 1..K
%
% Note: You can use a for-loop over the examples to compute this.
%

% number of examples 
m = size(X,1);

% set up distance matrix for each example, each centroid 
dist_array = zeros(m,K);

for i = 1:K
  dist_to_centroid = bsxfun(@minus, X, centroids(i,:));
  % need to minus every row of X by the centroid currently chosen in the loop (centroid K)   
  
  dist_array(:,i) = sum(dist_to_centroid.^2,2);
  % for that column of the Kth centroid in the dist_array, set it to
  % the sum of squared distances element wise, for every row
  % each row representing the element minus that Kth centroid 
endfor;

[min_value, indices] = min(dist_array, [], 2); 
idx = indices; 

% =============================================================

end;

