'''
Usage:  This script is to evaluate query and perform searching
        Use tf-idf or probability for ranking according to user's
        option. Rank the search results by score and return only
        top 100 results
        
Author: Jizhou Yang
Date:   12-21-2018
'''

from Process_Metadata import LoadMovie, Movie, Create_Index, ParseWords
from nltk.stem.snowball import SnowballStemmer
import re
import math
import random
from recomm import getRecommRate, movieDict


def QueryEvaluation(query, Index, Movies, userid, option):
    ''' read user's option and use desired algorithm '''
    if option == 'tf-idf':
        return tf_idf(query, Index, Movies, userid)
    elif option == 'language-model':
        return LanguageModel(query, Index, Movies, userid)
    else:
        pass    

def tf_idf(query, Index, Movies, userid):
    ''' tf-idf ranking algorithm '''
    
    st = SnowballStemmer("english") 
    terms = set()
    docs = set()
    
    # set movies and terms
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
                
        # to accommadate with recommendation system, check if the movie is in recommendation data
        if d in movieDict:
            ans.append(list([d, Movies[d].GetGenres(), Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score, getRecommRate(userid, d)]))
        else:
            ans.append(list([d, Movies[d].GetGenres(), Movies[d].GetTitle(), Movies[d].GetStar(), Movies[d].GetDirector(), score, float(0)]))
    
    # sort the results according to tf-idf score
    ans = sorted(ans, key=lambda x:x[-2], reverse=True)
    
    # return the top 100 results
    return ans[:100] 
            
            
def LanguageModel(query, Index, Movies, userid):
    ''' probability model for ranking '''
    ''' for each movie in movies, get the meta information, and probability of the counts '''
    
    lowpro = 0.000001   # default value when a word is not in the movie
    st = SnowballStemmer("english") 
    
    # process the query 
    terms = set()    
    for t in query.split():
        t = st.stem(t.lower())
        terms.add(t)
    
    # calculate probability for each movie
    ans = []
    for k, v in Movies.items():
        p = 1
        wl = v.GetWordList()
        for t in terms:
            if t in wl:
                p *= wl[t] / v.GetTotalCnt()
            else:
                p *= lowpro
        if v.GetId() in movieDict:
            ans.append(list([v.GetId(), v.GetGenres(), v.GetTitle(), v.GetStar(), v.GetDirector(), p, getRecommRate(userid, d)]))
        else:
            ans.append(list([v.GetId(), v.GetGenres(), v.GetTitle(), v.GetStar(), v.GetDirector(), p, float(0)]))
    
    # sort results by probability score  
    ans = sorted(ans, key=lambda x:x[-2], reverse=True)  
    
    # return top 100 results
    return ans[:100]
      
            


