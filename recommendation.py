recommendation index page 
provide a recomm-rate followed each search result
provide different catecory recomm index page

1.
# Transfer data to a matrix and filled missing data, such as fill 0s for all missing values
# Get Users-Movies-Ratings Dataset Matrix

2.
# Use collaborative filtering as my main strategy
# There are two directions in the collaborative filtering based recommendation systems, which are memory based and model based recommendation, I'm going to use Item-based 
# to find out the similarity between A movie and the target movie first. Then I used the similarity of the user's rating of A movie to get a prediction rating 
# that A movie can contribute to the target movie. Use such approach to traverse all movies and used the predictive weighted average as the final target rating.

3.
#Selection of similarity metric
#I'm going to use Cosine similarity, and will try use different similarity metrics such as Pearson similarity and Euclidean similarity in the recommendation engine.

4.
# root mean squared error (RMSE) to evaluate performance

5.
# ? Model based. Try to use singular value decomposition(SVD).

6. 
# ? Generate term vectors for each movie. It is based on top 10 terms of each movie's info. Then use above similarity metric to get similarity between movies. 
# And recommend movies which have high ismilarity with search result moives.  


# In[17]:



# coding: utf-8

# In[16]:


import random
from numpy import *
from pandas import *
from numpy import linalg as la
def getDataFrameFaster():
    data=DataFrame()  
    return mat(data.as_matrix()),movieid,userid


# In[18]:


myMat,movieDict,userDict=getDataFrameFaster()
print(myMat)
print(shape(myMat)[0])
print(shape(myMat)[1])


# In[19]:


def cosSim(inA,inB):  
    num=float(inA.T*inB)  
    denom=la.norm(inA)*la.norm(inB)  
    return 0.5+0.5*(num/denom) 


# In[20]:


n = np.shape(myMat)[1]
U,sigma,VT = np.linalg.svd(myMat)
sig4 = np.mat(np.eye(4)*sigma[:4])
xformedMovies = myMat.T * U[:,:4] * sig4


# In[21]:


def svdEst(dataSet,user,simMeans,movie):
#     n = np.shape(dataSet)[1]
#     U,sigma,VT = np.linalg.svd(dataSet)
#     sig4 = np.mat(np.eye(4)*sigma[:4])
#     xformedMovies = dataSet.T * U[:,:4] * sig4
#   xformedMovies is VT[:4,:].T
    simTotal = 0
    ratSimTotal = 0
    for i in range(n):
        userRating = dataSet[user,i]
        if userRating == 0 or i == movie:
            continue
        similarity = simMeans(xformedMovies[i,:].T,xformedMovies[movie,:].T)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal/simTotal


# In[22]:


def standEst(dataMat,user,simMeas,movie):
    n=shape(dataMat)[1]  
    simTotal=0.0  
    ratSimTotal=0.0  
    for j in range(n):  
        userRating=dataMat[user,j]    
        if userRating==0:continue  
        overLap=nonzero(logical_and(dataMat[:,movie].A>0,dataMat[:,j].A>0))[0]   
#         print('OVERLAP',overLap)  
        if len(overLap)==0:  
            similarity=0  
        else:  
            similarity=simMeas(dataMat[overLap,movie],dataMat[overLap,j])  # dataMat[overLap,movie] 
#         print('the %d and %d similarity is: %f' % (movie,j,similarity))  
        simTotal+=similarity                
        ratSimTotal+=similarity*userRating  
    if simTotal==0:                    
        return 0  
    else:  
        return ratSimTotal/simTotal   


# In[23]:


def recommend(user,N=20,simMeans = cosSim,estMethod = svdEst,dataSet=myMat):#recommendation engine
    unratedMovies = np.nonzero(dataSet[user,:]==0)[1]
    if len(unratedMovies) == 0:
        return 'every movie have been rate'
    movieScores = [] 
    for movie in unratedMovies:
        estimatedScore = estMethod(dataSet,user,simMeans,movie)
        movieScores.append((movieDict[movie],estimatedScore))
    return sorted(movieScores,key = lambda pp: pp[1],reverse = True)[:N]


# In[24]:


def getSum(dataMat,user,movie,simMeas=ecludSim,estMethod=standEst):  
    ori=dataMat[user,movie]        #save original review  
    dataMat[user,movie]=0          #set original review to 0  
    sim=standEst(dataMat, user, simMeas, movie)  #compute estimate review 
    dataMat[user,movie]=ori        #recover original review   
    return (ori-sim)**2           #error squared  


# In[31]:


def test(estMethod=standEst):  #testing RMSE   
    n=shape(myMat)[1]  
    m=shape(myMat)[0] 
    sumPears=0.0  
    sumEclud=0.0  
    sumCos=0.0  
    cnt=0  
    for i in [random.randint(0,m) for k in range(200)]:  
        for j in nonzero(myMat[i,:]>0)[1]:  
                sumPears+=getSum(myMat,i,j,simMeas=pearsSim,estMethod=estMethod)
                sumEclud+=getSum(myMat, i, j, simMeas=ecludSim,estMethod=estMethod)  
                sumCos+=getSum(myMat,i,j,simMeas=cosSim,estMethod=estMethod)  
                cnt+=1     
    return ((sumCos**0.5)/cnt),((sumPears**0.5)/cnt),((sumEclud**0.5)/cnt)


# In[37]:


recommend(6, 20, cosSim, standEst)


# In[35]:


test(svdEst)

