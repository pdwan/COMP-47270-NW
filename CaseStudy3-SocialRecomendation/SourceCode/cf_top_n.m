%{
    Author          Paula Dwan
	Email           paula.dwan@gmail.com
	Student ID      13208660

	Module          COMP47270 (Computational Network Analysis and Modeling)
	Course          MSc ASE
	Due date		11-May-2015
	Lecturer		Dr. Neil Hurley

	CASE STUDY 3	Social Recommendations
%}

%	calculate MAE using collaborative filtering
function cf_top_n
    global k;
    global n;
    k = 20;
    % k = 50;
    % k = 100;
    % k = 250;
    n = 5;			% top N ratings to use

    % srcRatings = load('../DataSets/ml.dat');
    srcRatings= load('../DataSets/epinions_rating_3.txt');

    p = randperm(length(srcRatings)); 		% use random permutations of srcRatings into p
    srcRatings(:,1) = srcRatings(p,1);
    srcRatings(:,2) = srcRatings(p,2);
    srcRatings(:,3) = srcRatings(p,3);
    numTrans = length(srcRatings);			% Five divisions : test  & train in turn
    division=floor(numTrans/5);
    first=1;
    final = division;
    sumAbsErr = 0;					% performance --> MAE
    totalTrans = 0;
    

    fileID = fopen('cf_top_n_results.txt', 'w');
    fprintf(fileID,'Calculating CF with TOP N for k = %d\n', k);

    fprintf('\n\nTO DATE : \n\t Total Trans \t\t MAE \n\t--------------------------------------------------- \n');
    fprintf(fileID,'\n\nTO DATE : \n\t Total Trans \t\t MAE \n\t--------------------------------------------------- \n');

    for i=1:5,		% use each fifth as test | training data in turn
    
        testSrc = srcRatings(first:final,:);
        trainSrc = [srcRatings(1:(first-1),:);srcRatings((final+1):end,:)];
    
        first = first+division;
        final = final+division;
    
        trainSet=sparse(trainSrc(:,1),trainSrc(:,2),trainSrc(:,3));
    
        % calculate CF Top N --> trainSet
        topNTrain=calculateTopNForTrainSet(trainSrc, trainSet);
    
        % calculate CF Top N --> testSet using Pearsons coefficient to 
        % get best match: did the training work?
        topNTest=calculateTopNForTestSetPearsons (testSrc, trainSrc);
    
        % calculate performance --> MAE
        if (topNTest == topNTrain), 		% get difference for Top N = 5
            diffAbsErr = 0;
        else
            diffAbsErr = ( abs(topNTrain(5)-topNTest(5)) + abs(topNTrain(4)-topNTest(4)) + abs(topNTrain(3)-topNTest(3)) + abs(topNTrain(2)-topNTest(2)) + abs(topNTrain(1)-topNTest(1))  ) / n;
            sumAbsErr = sumAbsErr+diffAbsErr;
            totalTrans = totalTrans + 1;
            if ( (mod(totalTrans,1000)) == 0 ),
                fprintf(fileID, '\t %d \t %e\n', totalTrans, sumAbsErr/totalTrans);
                fprintf('\t %d \t %e\n', totalTrans, sumAbsErr/totalTrans);
            end
        end
    end
    
    MAE = sumAbsErr/totalTrans;
    fprintf('\nFINAL RESULTS : \n\t---------------------------------------------------  \n');
    fprintf('\tMAE \t\t= %e\n', MAE);
    fprintf('where \tk \t\t= %d \n\tDataSet \t= %s \n\tactiveUser \t= %d \n\tactiveItem \t= %d \n\tactiveRating \t= %d \n', k, srcRatings,  activeUser, activeItem, activeRating);
    
    fprintf(fileID, '\nFINAL RESULTS : \n\t---------------------------------------------------  \n');
    fprintf(fileID, '\tMAE \t\t= %e\n', MAE);
    fprintf(fileID, 'where \tk \t\t= %d \n\tDataSet \t= %s \n\tactiveUser \t= %d \n\tactiveItem \t= %d \n\tactiveRating \t= %d \n', k, srcRatings,  activeUser, activeItem, activeRating);
    
    fclose(fileID);
    
%
%	calculate top N rating using training set
%
function topNTrain=calculateTopNForTrainSet(portion, set)
    global k;
    global n;
    
    for trans=1:length(portion),
        
        activeUser = portion(trans,1);
        activeItem = portion(trans,2);
        activeRating = portion(trans,3);
        
        sim = computeSimilarities(activeUser,set); % simularity : active user --> all training users
        sim(activeUser) = -1;			% set to < lowest --> move to bottom of list
        mask = set(:,activeItem) > 0;	% get actual rating, if does not exist then rating = 0
        sim(mask==0) = -1;			    %set to < lowest --> move to bottom of list
        [s,indx] = sort(sim,'descend');	% sorted order --> indexed array list of neighbors with best similarity
        neighbours = indx(1:k);		    % pick k most similar neighbours
        mask = sim(neighbours) > 0;     % remove any neighbours with no ratings (rating = 0)
        neighbours = neighbours(mask);	% neighbors rating listing
        
        
        if (isempty(neighbours)),        % if none then use midpoint
            predictRating = 3;
        else
            predictRating = round(mean(set(neighbours,activeItem)));
            if (predictRating > topNTrain(1)),
                topNTrain(5) = topNTrain(4);
                topNTrain(4) = topNTrain(3);
                topNTrain(3) = topNTrain(2);
                topNTrain(2) = topNTrain(1);
                topNTrain(1) = predictRating;
            elseif (predictRating > topNTrain(2)),
                topNTrain(5) = topNTrain(4);
                topNTrain(4) = topNTrain(3);
                topNTrain(3) = topNTrain(2);
                topNTrain(2) = predictRating;
            elseif predictRating > topNTrain(3),
                topNTrain(5) = topNTrain(4);
                topNTrain(4) = topNTrain(3);
                topNTrain(3) = predictRating;
            elseif predictRating > topNTrain(4),
                topNTrain(5) = topNTrain(4);
                topNTrain(4) = predictRating;
            elseif predictRating > topNTrain(5),
                topNTrain(5) =  predictRating;
            end
        end
    end
        
%
%	calculate top N using test data --> does Pearsons Correlation improve results
%
function topNTest=calculateTopNForTestSetPearsons(testPortion, trainPortion)
    
	global n
        
    dataPortion = length(trainPortion);
    startDataIndex=1;
    endDataIndex=dataPortion;
    pearsonCoefficient = -1;
    pearsonIndex = 1;
    
    for i=1:n-1,							% get best Pearson's Coefficient
    	testData(1, dataPortion) = testPortion(startDataIndex, endDataIndex);
        pearsons = cov(testData, trainPortion) / sqrt ( var(testData) * var(trainPortion)  );
        if (pearsons > pearsonCoefficient),
        	pearsonCoefficient = pearsons;
            pearsonIndex = startDataIndex;
        end
        startDataIndex = endDataIndex;
        endDataIndex = endDataIndex + dataPortion;
    end
    
    testData(1, dataPortion) = testPortion(pearsonIndex, pearsonIndex+dataPortion-1);
    for trans=1:dataPortion,				% get new active / current user
        activeUser = testData(trans:1);
        activeItem = testData(trans:2);
        activeRating = testData(trans:3);

        if (activeRating > topNTrain(1) && activeRating > topNTest(1)),
            topNTest(5) = topNTest(4);		% compare activeRating to training & test values
            topNTest(4) = topNTest(3);		% update test values if better
            topNTest(3) = topNTest(2);
            topNTest(2) = topNTest(1);
            topNTest(1) = activeRating;
        elseif (activeRating > topNTrain(2) && activeRating > topNTest(2)),
            topNTest(5) = topNTest(4);
            topNTest(4) = topNTest(3);
            topNTest(3) = topNTest(2);
            topNTest(2) = activeRating;
        elseif (activeRating > topNTrain(3) && activeRating > topNTest(3)),
            topNTest(5) = topNTest(4);
            topNTest(4) = topNTest(3);
            topNTest(3) = activeRating;
        elseif (activeRating > topNTrain(4) && activeRating > topNTest(4)),
            topNTest(5) = topNTest(4);
            topNTest(4) = predictRating;
        elseif (activeRating > topNTrain(5) && activeRating > topNTest(5)),
            topNTest(5) =  activeRating;
        end
    end
                    
function sim=computeSimilarities(user,trainSet)
    user_row = trainSet(user,:);
    sim = trainSet*user_row';