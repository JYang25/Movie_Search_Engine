'''
This script is to process the movie meta data

'''

import csv
import io
from nltk.stem.snowball import SnowballStemmer
import re

class Movie(object):
    def __init__(self):
        self.title = ''
        self.star = ''
        self.director = ''
        self.id = -1
        self.overview = ''
        self.popularity = 0
        self.vote = 0
        
    def GetTitle(self):
        return self.title
    
    def SetTitle(self, title):
        self.title = title
    
    def GetStar(self):
        return self.star
    
    def SetStar(self, star):
        self.star = star    
    
    def GetDirector(self):
        return self.director
    
    def SetDirector(self, director):
        self.director = director     
        
    def GetPopularity(self):
        return self.popularity
    
    def SetPopularity(self, popularity):
        self.popularity = popularity      
        
    def GetVote(self):
        return self.vote
    
    def SetVote(self, vote):
        self.vote = vote    
        
    def GetOverview(self):
        return self.overview
    
    def SetOverview(self, overview):
        self.overview = overview
    
    
class Idx(object):
    def __init__(self):
        self.cnt = 1
        self.tf = {}   # key: doc ID, value: count
        
    def GetCnt(self):
        return self.cnt
    
    def IncCnt(self):   # increase the count of a word by 1
        self.cnt += 1
        
    def AddId(self, movie_id):
        if movie_id in self.tf:
            self.tf[movie_id] += 1  # increase the count of this word in the specific movie
        else:
            self.tf[movie_id] = 1   # initiate as 1
            
    def GetTf(self):
        return self.tf
        
        

def LoadMovie():
    
    Movies = {}
    
    # use id to represent movie, hash table to a class of movie data
    
    # Load starring and director information
    with open('data/2/credits.csv', encoding="utf-8") as fin:
        csv_reader = csv.reader(fin, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
            #    print(row[0])
            #    print(row[1])
            #    print(row[2])
            #    print(type(row[2]), row[2])
                
                idx1 = row[0].find("'name':")
                idx2 = row[0][idx1:].find(',')
                star = row[0][idx1+9:idx1+idx2-1]    # remove the '' at begining and end
                
                # get star information
                if row[2] in Movies:
                    Movies[row[2]].SetStar(star)
                else:
                    Movies[row[2]] = Movie()
                    Movies[row[2]].SetStar(star)
                    
                # get director information
                idx3 = row[1].find("'Director', 'name':")
                idx4 = row[1][idx3+19:].find(',')
                director = row[1][idx3+21:idx3+19+idx4-1]    # remove the '' at begining and end   
                Movies[row[2]].SetDirector(director)
                
                
    # Load other meta data
    with open('data/2/movies_metadata.csv', encoding="utf-8") as fin:
        csv_reader = csv.reader(fin, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row) < 20:    # omit movies with incomplete information
                    continue
                
                # set title for the movie
                if row[5] in Movies:
                    Movies[row[5]].SetTitle(row[8])
                else:
                    Movies[row[5]] = Movie()
                    Movies[row[5]].SetTitle(row[8])
                
                # set overview for the movie
                Movies[row[5]].SetOverview(row[9])
                
                # set popularity
                Movies[row[5]].SetPopularity(row[10])
                
                # set vote
                Movies[row[5]].SetVote(row[22])
    
    return Movies            
                
#    for k, v in Movies.items():
#        print(k)
#        print(v.GetTitle(), v.GetStar(), v.GetDirector(), v.GetPopularity(), v.GetVote(), v.GetOverview())
    

def ParseWords(k, line, Index, st):
    line = re.sub(r'[\'|\d+|\-]', ' ', line)
    line = re.sub(r'[^(\w)|(\s+)]', '', line)
    arr = line.split()
    for w in arr:
        w = w.lower()
        w = st.stem(w)         
        if w not in Index:
            Index[w] = Idx()
        else:
            Index[w].IncCnt()
        Index[w].AddId(k)    

def Create_Index(Movies):
    st = SnowballStemmer("english")
    Index = {}   # an index for all the key words
    
    for k, v in Movies.items():
        # get words from title
        ParseWords(k, v.GetTitle(), Index, st)
        # get words from Starring
        ParseWords(k, v.GetStar(), Index, st)
        # get words from Director
        ParseWords(k, v.GetDirector(), Index, st)     
        # get words from Overview
        ParseWords(k, v.GetOverview(), Index, st)           
 
    return Index        
       
#    for k2, v2 in Index.items():
#        print(k2, v2.GetTf())
                

M = LoadMovie()

I = Create_Index(M)



