'''
Usage: This script is to process the movie meta data, construct the index for search engine.
       Movie is a class to hold the movie meta data. Idx is a class to hold word frequency 
       and which movie has this word. When we start the system, this script read the csv files
       to construct the two indices.
       
Author: Jizhou Yang
Date:   12-21-2018
'''

import csv
import io
from nltk.stem.snowball import SnowballStemmer
import re
import json
from csv import reader


class Movie(object):
    ''' This class contains movie meta data. This class is used for index construction '''
    ''' Where key is the movie id and the value is this class '''
    
    def __init__(self):
        ''' initiate the class with default meta data '''
        self.title = ''
        self.star = ''
        self.director = ''
        self.id = -1
        self.overview = ''
        self.popularity = 0
        self.vote = 0
        self.genres = 'Other'
        
        # this value is for language model
        # get total number of words in a document
        self.totalcount = 0
        
        # a word list of count of each word in a movie
        self.wordlist = {}
        
    def GetGenres(self):
        ''' Get the genres of this movie '''
        return self.genres

    def SetGenres(self, genres):
        ''' Set the genres according to movie genres data '''
        # check the genres from input 
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
        ''' set movie id '''
        self.id = id
    
    def GetId(self):
        ''' get movie id '''
        return self.id
    
    def GetWordList(self):
        ''' get word list of movie '''
        return self.wordlist
        
    def AddWordList(self, w):
        ''' add a word to the movie's word list '''
        if w in self.wordlist:
            self.wordlist[w] += 1
        else:
            self.wordlist[w] = 1
    
    def IncTotalCnt(self, cnt):
        ''' increase the total count of a word '''
        self.totalcount += cnt
    
    def GetTotalCnt(self):
        ''' get the total count of words of this movie '''
        return self.totalcount
        
    def GetTitle(self):
        ''' get the title of this movie '''
        return self.title
    
    def SetTitle(self, title):
        ''' set title for this movie '''
        self.title = title
    
    def GetStar(self):
        ''' get the star of this movie '''
        return self.star
    
    def SetStar(self, star):
        ''' set star for this movie '''
        self.star = star    
    
    def GetDirector(self):
        ''' get director of this movie '''
        return self.director
    
    def SetDirector(self, director):
        ''' set director for this movie '''
        self.director = director     
        
    def GetPopularity(self):
        ''' get popularity score '''
        return self.popularity
    
    def SetPopularity(self, popularity):
        ''' set popularity score '''
        self.popularity = popularity      
        
    def GetVote(self):
        ''' get vote value of this movie '''
        return self.vote
    
    def SetVote(self, vote):
        ''' set vote value of this movie '''
        self.vote = vote    
        
    def GetOverview(self):
        ''' get overview of this movie '''
        return self.overview
    
    def SetOverview(self, overview):
        ''' set overview for this movie '''
        self.overview = overview
    
    
class Idx(object):
    ''' This class is also for index construction '''
    ''' where the key is a word, and the value is this class '''
    ''' to record which movie contains this word, and the total '''
    ''' count of this word in the whole dataset '''
    
    def __init__(self):
        ''' initiate the class with default value '''
        self.cnt = 1
        self.tf = {}   # term frequency of this word in each movie. key: doc ID, value: count
        
    def GetCnt(self):
        ''' get count of this word '''
        return self.cnt
    
    def IncCnt(self):
        ''' increase the count of word by 1 '''
        self.cnt += 1
        
    def AddId(self, movie_id):
        ''' add a movie id into term frequency dictionary '''
        ''' when the movie contains this word '''
        if movie_id in self.tf:
            self.tf[movie_id] += 1  # increase the count of this word in the specific movie
        else:
            self.tf[movie_id] = 1   # initiate as 1
            
    def GetTf(self):
        ''' get total frequency of a word '''
        return self.tf
        
        

def LoadMovie():
    ''' read the csv file and construct index '''
    Movies = {} # key is movie id, value is Movie class
    
    # Load starring and director information
    with open('./data/credits.csv', encoding="utf-8") as fin:
        csv_reader = csv.reader(fin, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
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
                           
    # Load other movie meta data
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

                # set overview for the movie
                Movies[row[5]].SetOverview(row[9])
                
                # set popularity
                Movies[row[5]].SetPopularity(row[10])
                
                # set vote
                Movies[row[5]].SetVote(row[22])
                
                # set id
                Movies[row[5]].SetId(row[5])               
    
    return Movies            
                    

def ParseWords(k, line, Index, st, v):
    ''' parse the text of movie meta data '''
    
    # remove symbols and extra spaces in the string
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
    ''' create index from movie data '''
    
    # initiate stem function
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
       

# run the script to construct index and assign to variable 'M' and 'I'
M = LoadMovie()
I = Create_Index(M)

