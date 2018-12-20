import csv
import random
from numpy import *
from pandas import *
from numpy import linalg as la
from Process_Metadata import LoadMovie, M
from data_frame import ratingMat,movieDict,userDict

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

def standEst(dataMat,user,simMeas,item):  
    n=shape(dataMat)[1]  
    simTotal=0.0  
    ratSimTotal=0.0  
    for j in range(n):  
        userRating=dataMat[user,j]   
        if userRating==0:continue  
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0] 
#         print('OVERLAP',overLap)  
        if len(overLap)==0:  
            similarity=0  
        else:  
            similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])  # dataMat[overLap,item] 
#         print('the %d and %d similarity is: %f' % (item,j,similarity))  
        simTotal+=similarity                 
        ratSimTotal+=similarity*userRating 
    if simTotal==0:                    
        return 0  
    else:  
        return ratSimTotal/simTotal  


def recommend(userid, N=20, simMeans = cosSim, estMethod = standEst, dataSet=ratingMat, genre=""):#推荐引擎
    unratedItems = np.nonzero(dataSet[userid,:]==0)[1]
    if len(unratedItems) == 0:
        return 'every movie have been rate'
    itemScores = [] 
    for item in unratedItems:
        if str(movieDict[item]) in M:
            if genre != "":
                if M[str(movieDict[item])].GetGenres() == genre:
                    estimatedScore = float("{0:.2f}".format(estMethod(dataSet,userid,simMeans,item)))
                    if estimatedScore > 0:
                        itemScores.append((movieDict[item],estimatedScore))
            else:
                estimatedScore = float("{0:.2f}".format(estMethod(dataSet,userid,simMeans,item)))
                if estimatedScore > 0:
                    itemScores.append((movieDict[item],estimatedScore))
        
            # print(M[str(movieDict[item])].GetGenres())
        
    return sorted(itemScores,key = lambda pp: pp[1],reverse = True)[:N]

def recommTop20(userid, metric):
    if metric == "cosine":
        return recommend(int(userid), 100, cosSim, standEst)
    elif metric == "pearson":
        return recommend(int(userid), 100, pearsSim, standEst)
    elif metric == "euclidean":
        return recommend(int(userid), 100, ecludSim, standEst)

def recommByGenre(userid, genre):
    return recommend(int(userid), 100, cosSim, standEst, ratingMat, genre)

def getRecommRate(userid, movieid):
    return float("{0:.2f}".format(standEst(ratingMat, int(userid), cosSim, int(movieid))))
