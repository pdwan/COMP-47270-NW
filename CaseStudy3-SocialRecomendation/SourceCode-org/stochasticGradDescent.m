function stochasticGradDescent
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
ratingTest=false;
rankingTest=true;

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
    
    % err is the some of the square errors
    err=full(sum(sum(E.*E)));
    
    
    fprintf('Initial root mean squared error : %e\n', sqrt(err/nnz(E)))
    
    %% Training Phase -- 
    
    lambda = 0.02; % penalty term
    alpha = 0.005;  % learning rate
    numPasses = 10;
    for pass=1:numPasses,
        pass
        
        % permute the order in which the data is accessed
        prm = randperm(length(row));
        err=0;
        for i=1:length(row),
            user = row(prm(i));
            item = col(prm(i));
            
            
            % update the error -- after P(user,:) and Q(item,:) are updated,
            % the error needs to be updated - we always use the most
            % up-to-date value for E(user,item)
            E(user,item) = R(user,item)-P(user,:)*Q(item,:)';
           
            err= err + E(user,item)^2;
            
            % update rule with gradient approximated 
            P(user,:) = P(user,:)+alpha*(E(user,item)*Q(item,:)-lambda*P(user,:));
            Q(item,:) = Q(item,:)+alpha*(E(user,item)*P(user,:)-lambda*Q(item,:));
            
            
        end
        
        
        fprintf('Training Mean squared after %d passes is %e\n', pass,sqrt(err/nnz(E)));
    end
    
    %% Testing Phase
    
    
    if (ratingTest)
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
    else
        if (rankingTest)
            rankTestSet = testSet;
            rankTestSet(rankTestSet<4 & rankTestSet>0)=-1;
            rankTestSet(rankTestSet>=4)=1;
            
            for i=1:nusers,
                nrated=sum(rankTestSet(i,:)==1);
                mask=(rankTestSet(i,:)==1 |rankTestSet(i,:)==-1);
                candidates=find(rankTestSet(i,:)==0);
                prm=randperm(length(candidates));
                s=min(length(candidates),nrated);
                rankTestSet(i,candidates(prm(1:s)))=2;
            end
            
            for i=1:nusers,
                i
                candidates=find(rankTestSet(i,:)==1 | rankTestSet(i,:)==2);
                nrated = sum(rankTestSet(i,candidates)==1);
                
                if (length(candidates)>0)
                    ratings=zeros(length(candidates),1);
                    realratings=zeros(length(candidates),1);
                    for j=1:length(candidates),
                        ratings(j) = P(i,:)*Q(candidates(j),:)';
                        realratings(j) = rankTestSet(i,candidates(j));
                    end
                    [s,indx]=sort(ratings,'descend');
                    errorrate = sum(realratings(indx(1:nrated))~=1)/nrated;
                    
                    testerr = testerr + errorrate;
                    numTests = numTests+1;
                end
            end
            fprintf('Mean square error on cross validation pass %d is %e\n',  ...
                crossvalpass, testerr/numTests);
        end
    end
end
