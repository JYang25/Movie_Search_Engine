from Process_Metadata import LoadMovie, Movie, Create_Index, ParseWords, Idx, M, I
from nltk.stem.snowball import SnowballStemmer
import re
import math

from recomm import getRecommRate





def QueryEvaluation(query, Index, Movies, userid):
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
        score += float(Movies[d].GetPopularity()) + float(Movies[d].GetVote())
        
        ans.append(list([d, M[d].GetTitle(), M[d].GetStar(), M[d].GetDirector(), score, getRecommRate(userid, d)]))
        
    ans = sorted(ans, key=lambda x:x[-1], reverse=True)
    
    # print(ans)
    return ans        
    
            
QueryEvaluation('Caesar Rome', I, M)            
            







