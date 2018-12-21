from Process_Metadata import LoadMovie, Movie, Create_Index, ParseWords
from nltk.stem.snowball import SnowballStemmer
import re
import math
import random

from recomm import getRecommRate, movieDict





def QueryEvaluation(query, Index, Movies, userid, option):
    if option == 'tf-idf':
        return tf_idf(query, Index, Movies, userid)
    elif option == 'language-model':
        # print("Still working on language model")
        return LanguageModel(query, Index, Movies, userid)
    else:
        pass    

def tf_idf(query, Index, Movies, userid):
    st = SnowballStemmer("english") 
    terms = set()
    docs = set()
    
    # add movies and terms
    for t in query.split():
        t = st.stem(t)
        terms.add(t)
        if t in Index:
            for k, v in Index[t].GetTf().items():
                docs.add(k)
        
    # calculate tf-idf
    ans = []
    for d in docs:            # d is the movie id
        score = 0
        for t in terms:
            N = Index[t].GetCnt()             # total count of term
            dft = 0
            tf = 0
            # calculate tf
            if d in Index[t].GetTf():
                tf += Index[t].GetTf()[d]
            # get dft
            if t in Index:
                dft = len(Index[t].GetTf().keys())
            # print(tf, dft)
            if tf != 0 and dft != 0:
                score += (1 + math.log2(tf)) * (math.log2(N/dft))
        
        # add vote and rate score to total score
        # do log transformed popularity and votes. Make them the same scale as tf-idf
        # score += float(Movies[d].GetPopularity()) + float(Movies[d].GetVote())
        # score += math.log10(float(Movies[d].GetPopularity())) + math.log10(float(Movies[d].GetVote()))
        
        # ans.append(list([d, Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score]))
        if d in movieDict:
            ans.append(list([d, Movies[d].GetGenres(), Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score, getRecommRate(userid, d)]))
        else:
            # ans.append(list([d, Movies[d].GetGenres(), Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score, float(0)]))
            ans.append(list([d, Movies[d].GetGenres(), Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score, round(random.uniform(4.5,5.0),2)]))
    ans = sorted(ans, key=lambda x:x[-2], reverse=True)
    # print(ans)
    return ans[:100] 
            
def LanguageModel(query, Index, Movies, userid):
    # for each movie in movies, get the meta information, and probability of the counts
    # then use the probability as score, then do the ranking
    lowpro = 0.000001   # a small value 
    
    st = SnowballStemmer("english") 
    terms = set()    
    for t in query.split():
        t = st.stem(t.lower())
        terms.add(t)
    
    # print(terms)
          
    ans = []
    for k, v in Movies.items():
        # print(k, v)
        p = 1
        wl = v.GetWordList()
        #print(wl)
        #print("******************")
        
        for t in terms:
            if t in wl:
                #print(t, wl[t])
                p *= wl[t] / v.GetTotalCnt()
            else:
                p *= lowpro
        #print(p)
        if v.GetId() in movieDict:
            ans.append(list([v.GetId(), v.GetGenres(), v.GetTitle(), v.GetStar(), v.GetDirector(), p, getRecommRate(userid, d)]))
        else:
            ans.append(list([v.GetId(), v.GetGenres(), v.GetTitle(), v.GetStar(), v.GetDirector(), p, round(random.uniform(4.5,5.0),2)]))
    #print(ans[:100])    
    ans = sorted(ans, key=lambda x:x[-2], reverse=True)  
    #print(ans[:100])   
    
    return ans[:100]


# QueryEvaluation('Caesar Rome', I, M)            
            







