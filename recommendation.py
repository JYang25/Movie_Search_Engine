# recommendation index page 
# provide a recomm-rate followed each search result
# provide different catecory recomm index page
# public recomm-rate:
# private recomm-rate:

# 1.
# # Transfer data to a matrix and filled missing data, such as fill 0s for all missing values
# # Get Users-Movies-Ratings Dataset Matrix

# 2.
# # Use collaborative filtering as my main strategy
# # There are two directions in the collaborative filtering based recommendation systems, which are memory based and model based recommendation, I'm going to use Item-based 
# # to find out the similarity between A movie and the target movie first. Then I used the similarity of the user's rating of A movie to get a prediction rating 
# # that A movie can contribute to the target movie. Use such approach to traverse all movies and used the predictive weighted average as the final target rating.

# 3.
# #Selection of similarity metric
# #I'm going to use Cosine similarity, and will try use different similarity metrics such as Pearson similarity and Euclidean similarity in the recommendation engine.

# 4.
# # root mean squared error (RMSE) to evaluate performance

# 5.
# # ? Model based. Try to use singular value decomposition(SVD).

# 6. 
# # ? Generate term vectors for each movie. It is based on top 10 terms of each movie's info. Then use above similarity metric to get similarity between movies. 
# # And recommend movies which have high ismilarity with search result moives.  


import csv
import random
from numpy import *
from pandas import *
from numpy import linalg as la
from Process_Metadata import LoadMovie, M

def getDataFrame():
    with open('./data/ratings_test.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        data=DataFrame() 
        for row in csv_reader:
            if line_count != 0:
                data.loc[int(row[0]),int(row[1])] = float(row[2]) 
            else:
                print(f'Column names are {", ".join(row)}')
            line_count += 1
        _=data.fillna(0,inplace=True)  
        movieid={}  
        userid={}  
        for i in range(len(data.columns)):  
            movieid[i]=data.columns[i]  
        for i in range(len(data.index)):  
            userid[i]=data.index[i]
        print(f'Processed {line_count} lines.')
    return mat(data.as_matrix()),movieid,userid

myMat,movieDict,userDict=getDataFrame()
print(myMat)
print(shape(myMat)[0])
print(shape(myMat)[1])

def cosSim(inA,inB):  
    num=float(inA.T*inB)  
    denom=la.norm(inA)*la.norm(inB)  
    return 0.5+0.5*(num/denom) 

def pearsSim(inA,inB):  
    if len(inA)<3:    
        return 1.0  
    if sum(var(inA))==0 or sum(var(inB))==0:  
        return 0  
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]  #2*2 matrix need to [0][1] 

def ecludSim(inA,inB):  
    return 1.0/(1.0+la.norm(inA-inB)) 

def standEst(dataMat,user,simMeas,item): #计算这个item对某用户的相似度，预测评分  
    n=shape(dataMat)[1]  
    simTotal=0.0  
    ratSimTotal=0.0  
    for j in range(n):  
        userRating=dataMat[user,j]  #找该用户评过分的物品  
        if userRating==0:continue  
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0] #评过分的物品和某item都取用户评分不为0的项计算相似度  
#         print('OVERLAP',overLap)  
        if len(overLap)==0:  
            similarity=0  
        else:  
            similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])  # dataMat[overLap,item] 
#         print('the %d and %d similarity is: %f' % (item,j,similarity))  
        simTotal+=similarity                #累加相似度  
        ratSimTotal+=similarity*userRating  #相似度乘以评分  
    if simTotal==0:                    
        return 0  
    else:  
        return ratSimTotal/simTotal  #得到预测评分 


def recommend(userid, N=20, simMeans = cosSim, estMethod = standEst, dataSet=myMat):#推荐引擎
    unratedItems = np.nonzero(dataSet[userid,:]==0)[1]
    if len(unratedItems) == 0:
        return 'every movie have been rate'
    itemScores = [] 
    for item in unratedItems:
        estimatedScore = float("{0:.2f}".format(estMethod(dataSet,userid,simMeans,item)))
        itemScores.append((movieDict[item],estimatedScore))
    return sorted(itemScores,key = lambda pp: pp[1],reverse = True)[:N]

recommend_list = recommend(1, 100, cosSim, standEst)

for m in recommend_list:
    if str(m[0]) in M:
        print(f' -  [{M[str(m[0])].GetTitle()}] | Director: {M[str(m[0])].GetDirector()} | Star: {M[str(m[0])].GetStar()} | Recommend(0-5): {m[1]}')