function gradDescentFactorisation
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
sumAbsErr = 0;
totalTrans = 0;


testerr=0;
numTests=0;

for crossvalpass=1:5,
    %% Start of crossvalidation pass
    
    testY = Y(first:last,:);
    trainY = [Y(1:(first-1),:);Y((last+1):end,:)];
    first = first+testSize;
    last = first+testSize-1;

    trainSet = sparse(trainY(:,1),trainY(:,2),trainY(:,3));
    testSet = sparse(testY(:,1),testY(:,2),testY(:,3));
    
    nusers = size(trainSet,1);
    nitems = size(trainSet,2);
    
    % firstly modify trainSet by subtracting the user means
    
    userMean = sum(trainSet,2)./sum(trainSet>0,2);
    
    R = trainSet;% - sparse(1:nusers,1:nusers,userMean)*spones(trainSet);
    
    %% Initialisation
    
    k = 20; % k is the number of categories
    
    
 % Initialise P and Q to uniform random numbers between 0 and 1
    
    P = rand(nusers,k);
    Q = rand(nitems,k);
    
  
    % compute two arrays, row and col that hold the indices of the non-zero
    % ratings in R
    [row,col]=find(R);    
    
    
    
    Rhat = spones(R);
    
    for i=1:length(row),
        Rhat(row(i),col(i)) = P(row(i),:)*Q(col(i),:)';
    end
    
    E  = R - Rhat;
    err=full(sum(sum(E.*E)));
    fprintf('Initial root mean squared error : %e\n', sqrt(err/nnz(E)));
    
    %% Training Phase
    numIters = 20;
    
    % penalty term 
    lambda = 0.02;  
    
    % learning rate -- need to choose alpha sufficiently small so that next step moves objective downwards
    alpha = 0.0001;  
    
    for iter=1:numIters,
        iter
        
        Pnew = P + alpha*(E*Q - lambda*P);
        Qnew = Q + alpha*(E'*P - lambda*Q);
        
        for i=1:length(row),
            Rhat(row(i),col(i)) = Pnew(row(i),:)*Qnew(col(i),:)';
        end
        
        E = R - Rhat;
        err = full(sum(sum(E.*E)));
        P = Pnew;
        Q = Qnew;
        
        fprintf('Training Mean squared after %d iterations is %e\n', iter,sqrt(err/nnz(E)));
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


      