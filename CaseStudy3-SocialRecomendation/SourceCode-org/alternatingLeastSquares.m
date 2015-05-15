function alternatingLeastSquares
Y = load('ml.dat');

p = randperm(length(Y));

Y(:,1) = Y(p,1);
Y(:,2) = Y(p,2);
Y(:,3) = Y(p,3);

% split into 5 sets

numTrans = length(Y);

first=1;
testSize=floor(numTrans/5);
last = first+testSize-1;


testerr=0;
numTests=0;

for crossvalpass=1:5,
    
    testY = Y(first:last,:);
    trainY = [Y(1:(first-1),:);Y((last+1):end,:)];
    first = first+testSize;
    last = first+testSize-1;

    trainSet = sparse(trainY(:,1),trainY(:,2),trainY(:,3));
    testSet = sparse(testY(:,1),testY(:,2),testY(:,3));
    
    nusers = size(trainSet,1);
    nitems = size(trainSet,2);
    
    
   
    R = trainSet;
    
    
   
    k = 20; % k is the number of categories
    
    
   
   %% Initialisation  
    
    % Initialise P and Q to uniform random numbers between 0 and 1
    
    P = rand(nusers,k);
    Q = rand(nitems,k);
   
    % compute two arrays, row and col that hold the indices of the non-zero
    % ratings in R
    [row,col]=find(R);
    
    
    % Rhat is the estimated ratings -- initialise a sparse matrix of same
    % structure as R, containing all ones
    Rhat = spones(R);
    
    % now fill Rhat with the estimated ratings
   
    for i=1:length(row),
        Rhat(row(i),col(i)) = P(row(i),:)*Q(col(i),:)';
    end
    
    % E contains the error - difference between R and Rhat
    E  = R - Rhat;
    
    % err is the sum of the square errors
    err=full(sum(sum(E.*E)));
    
    
    fprintf('Initial root mean squared error : %e\n', sqrt(err/nnz(E)));
    
    S = spones(R);
    
 
  %% Training Phase  
    lambda = 0.02; % penalty term
    numIters = 10;

    for iter=1:numIters,
                
        for i=1:nitems
            M = lambda*eye(k,k) + P'*diag(S(:,i))*P;
            Q(i,:) = M \ (P'*diag(S(:,i))*R(:,i));
        end
        
        for u=1:nusers
            M = lambda*eye(k,k) + Q'*diag(S(u,:))*Q;
            P(u,:) = M \ (Q'*diag(S(u,:))*R(u,:)');
        end
        
        for i=1:length(row),
            Rhat(row(i),col(i)) = P(row(i),:)*Q(col(i),:)';
        end
            
        E  = R - Rhat;
        
        % err is the sum of the square errors
        err=full(sum(sum(E.*E)));
        
        
        fprintf('Root mean squared error after %d iterations is : %e\n', iter, sqrt(err/nnz(E)));
        
    end
    
    
    %% Testing Phase
    
    % Get the row and col indices of the testSet ratings
    [row, col] = find(testSet);
   	
    % compute an prediction for each rating in the testSet and add
    % the difference in the rating and the prediciton into the testerr.
    for i=1:length(row),
        user = row(i);
        item = col(i);
        
        testerr = testerr + (testSet(user,item) - P(user,:)*Q(item,:)')^2;
        
        numTests = numTests+1;
    end
   
    fprintf('Mean square error on cross validation pass %d is %e\n',  ...
        crossvalpass, sqrt(testerr/numTests));
end

