'''
This script is to process the movie meta data

'''

import csv
import io
from nltk.stem.snowball import SnowballStemmer
import re
import json
from csv import reader


class Movie(object):
    def __init__(self):
        self.title = ''
        self.star = ''
        self.director = ''
        self.id = -1
        self.overview = ''
        self.popularity = 0
        self.vote = 0
        self.genres = 'Other'
        
        # for language model
        # get total number of words in a document
        self.totalcount = 0
        
        # a word list of count of each word in a movie
        self.wordlist = {}
        
    def GetGenres(self):
        return self.genres

    def SetGenres(self, genres):
        #print(genres)
        # read genres information from the string
        if genres.find('Comedy') != -1:
            self.genres = 'Comedy'
        elif genres.find('Horror') != -1:
            self.genres = 'Horror'
        elif genres.find('Animation') != -1:
            self.genres = 'Animation'
        elif genres.find('History') != -1:
            self.genres = 'History'
        elif genres.find('Drama') != -1:
            self.genres = 'Drama'
        elif genres.find('Action') != -1:
            self.genres = 'Action'  
        elif genres.find('Adventure') != -1:
            self.genres = 'Adventure'
        elif genres.find('Crime') != -1:
            self.genres = 'Crime'  
        elif genres.find('Romance') != -1:
            self.genres = 'Romance'  
        elif genres.find('Thriller') != -1:
            self.genres = 'Thriller'  
        elif genres.find('Fantasy') != -1:
            self.genres = 'Fantasy'  
        elif genres.find('Family') != -1:
            self.genres = 'Family'  
        elif genres.find('Fiction') != -1:
            self.genres = 'Fiction'  
            
        elif genres.find('Mystery') != -1:
            self.genres = 'Mystery'  
            
        elif genres.find('War') != -1:
            self.genres = 'War'  
            
        elif genres.find('Music') != -1:
            self.genres = 'Music'      
            
        elif genres.find('Documentary') != -1:
            self.genres = 'Documentary'            
            
        elif genres.find('Foreign') != -1:
            self.genres = 'Foreign'       
        else:
            self.genres = 'Other'  
        
        
        
    def SetId(self, id):
        self.id = id
    
    def GetId(self):
        return self.id
    
    def GetWordList(self):
        return self.wordlist
        
    def AddWordList(self, w):
        if w in self.wordlist:
            self.wordlist[w] += 1
        else:
            self.wordlist[w] = 1
    
    def IncTotalCnt(self, cnt):
        self.totalcount += cnt
    
    def GetTotalCnt(self):
        return self.totalcount
        
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
    with open('./data/credits.csv', encoding="utf-8") as fin:
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
    with open('./data/movies_metadata.csv', encoding="utf-8") as fin:
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
                
                # set genres for the movie  
                Movies[row[5]].SetGenres(row[3])
                #print(Movies[row[5]].GetTitle(), Movies[row[5]].GetId())
                #print(Movies[row[5]].GetGenres())
                
                
                # set overview for the movie
                Movies[row[5]].SetOverview(row[9])
                
                # set popularity
                Movies[row[5]].SetPopularity(row[10])
                
                # set vote
                Movies[row[5]].SetVote(row[22])
                
                # set id
                # set id 
                Movies[row[5]].SetId(row[5])               
    
    return Movies            
                
#    for k, v in Movies.items():
#        print(k)
#        print(v.GetTitle(), v.GetStar(), v.GetDirector(), v.GetPopularity(), v.GetVote(), v.GetOverview())
    

def ParseWords(k, line, Index, st, v):
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
        
        # add this word to the word list of the movie
        # v is the Movie class
        v.AddWordList(w)
        
        
    # get the length of the arr for word count of a movie
    return len(arr)

def Create_Index(Movies):
    st = SnowballStemmer("english")
    Index = {}   # an index for all the key words
    
    for k, v in Movies.items():
        # get words from title
        v.IncTotalCnt(ParseWords(k, v.GetTitle(), Index, st, v))
        # get words from Starring
        v.IncTotalCnt(ParseWords(k, v.GetStar(), Index, st, v))
        # get words from Director
        v.IncTotalCnt(ParseWords(k, v.GetDirector(), Index, st, v))     
        # get words from Overview
        v.IncTotalCnt(ParseWords(k, v.GetOverview(), Index, st, v))           
 
    return Index        
       
#    for k2, v2 in Index.items():
#        print(k2, v2.GetTf())
                


M = LoadMovie()
I = Create_Index(M)
# print(M['862'].GetTotalCnt())
# print(M['862'].GetWordList())
# print(M['9091'].GetTotalCnt())
# print(M['9091'].GetWordList())
