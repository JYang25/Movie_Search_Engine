import csv
from numpy import *
from pandas import *
from numpy import linalg as la
from Process_Metadata import LoadMovie

def getDataFrame():
    with open('./data/ratings_test.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        data=DataFrame() 
        for row in csv_reader:
            if line_count != 0:
                data.loc[int(row[0]),int(row[1])] = float(row[2]) 
            else:
                print("")
                # print(f'Column names are {", ".join(row)}')
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

ratingMat,movieDict,userDict=getDataFrame()
# print(ratingMat)
# print(f'{shape(ratingMat)[0]} users')
# print(shape(ratingMat)[1])