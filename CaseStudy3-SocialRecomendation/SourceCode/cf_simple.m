%{
	Author          Paula Dwan
	Email           paula.dwan@gmail.com
    Student ID      13208660

	Module          COMP47270 (Computational Network Analysis and Modeling)
	Course          MSc ASE
	Due date       11-May-2015
	Lecturer       Dr. Neil Hurley

	CASE STUDY 3	Social Recommendations
%}

%	calculate MAE using collaborative filtering
function cf_simple

% src = load('../DataSets/ml.dat');
% src = load('../DataSets/ep.dat');
src = load('../DataSets/epinions_rating_3.txt');

% k = 20;
% k = 50;
% k = 100;
k = 250;

p = randperm(length(src));	% use random permutations of srcDatset into p
src(:,1) = src(p,1);
src(:,2) = src(p,2);
src(:,3) = src(p,3);

numTrans = length(src);     % Five divisions : test  & train in turn
division=floor(numTrans/5);
first=1;
final = division;

sumAbsErr = 0;              % performance --> MAE
totalTrans = 0;

fileID = fopen('cf_results.txt', 'w');
fprintf(fileID,'Calculating CF SIMPLE for k = %d\n', k);

fprintf(fileID,'\n\nTO DATE : \n\t Total Trans \t\t MAE \n\t------------------------------------------------------------------------------------------------------ \n');
fprintf('\n\nTO DATE : \n\t Total Trans \t\t MAE \n\t------------------------------------------------------------------------------------------------------ \n');

for i=1:5,
    
    testSrcDataset = src(first:final,:);
    trainSrcDataset = [src(1:(first-1),:);src((final+1):end,:)];
    first = first+division;
    final = final+division;
    
    trainSet = sparse(trainSrcDataset(:,1),trainSrcDataset(:,2),trainSrcDataset(:,3));
    testSet = sparse(testSrcDataset(:,1),testSrcDataset(:,2),testSrcDataset(:,3));
    
    for trans=1:length(testSrcDataset),
        
        activeUser = testSrcDataset(trans,1);
        activeItem = testSrcDataset(trans,2);
        activeRating = testSrcDataset(trans,3);
        
        sim = computeSimilarities(activeUser,trainSet);		% simularity : active user --> all training users
        sim(activeUser) = -1;				% set to < lowest --> move to bottom of list
        mask = trainSet(:,activeItem) > 0;	% get actual rating, if does not exist then rating = 0
        sim(mask==0) = -1;			    	%set to < lowest --> move to bottom of list
        [s,indx] = sort(sim,'descend');		% sorted order --> indexed array list of neighbors with best similarity
        
        neighbours = indx(1:k);		    	% pick k most similar neighbours
        mask = sim(neighbours) > 0;     	% remove any neighbours with no ratings (rating = 0)
        neighbours = neighbours(mask);      % neighbors rating listing
        
        if (isempty(neighbours))			% if none then use midpoint
            predictRating = 3;
        else
            predictRating = round(mean(trainSet(neighbours,activeItem)));
        end
        
        sumAbsErr = sumAbsErr+abs(predictRating-activeRating);	% performance --> MAE
        totalTrans = totalTrans + 1;
        modTrans = mod(totalTrans,1000);
        if (modTrans == 0)
            fprintf(fileID, '\t %d \t %e\n', totalTrans, sumAbsErr/totalTrans);
            fprintf('\t %d \t %e\n', totalTrans, sumAbsErr/totalTrans);
        end
    end
end

MAE = sumAbsErr/totalTrans;
fprintf(fileID, '\nFINAL RESULTS :-\n---------------------------------------------------------------------------------------------------- \n');
fprintf(fileID, 'MAE \t\t= %e\n', MAE);
fprintf(fileID, '\twhere \tk = %d  \tDataSet = %s  \tactiveUser = %d  \tactiveItem = %d  \tactiveRating = %d \n', k, src, activeUser, activeItem, activeRating);

fprintf('\nFINAL RESULTS :-\n---------------------------------------------------------------------------------------------------- \n');
fprintf('\tMAE \t\t= %e\n', MAE);
fprintf('where \tk \t\t= %d \n\tDataSet = %s \n\tactiveUser = %d \n\tactiveItem = %d \n\tactiveRating = %d \n', k, src, activeUser, activeItem, activeRating);

fclose(fileID);

function sim=computeSimilarities(user,trainSet)
user_row = trainSet(user,:);
sim = trainSet*user_row';