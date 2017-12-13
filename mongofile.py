import psycopg2
import os
import csv
import io
from pymongo import MongoClient

def check():
    print("\n\n\n\n\n\n...............................MONGO DB CONNECTIVITY ESTABLISHED!............................... ")

def initMongo():
    con = MongoClient()

    db = con.finalproject1
    movies = db.movies
    movies.drop()
    
    
    #'column_name = {UserID,MovieID,Tag,Timestamp}'
    
    #path = "D:\\Fall 2017\\Database Systems\\Project-Main\\tags.csv"
    with io.open("tags.csv", errors = 'ignore') as f:
        csv_f = csv.reader(f)
        for i, row in enumerate(csv_f):
            if i > 1 and len(row) > 1:
                #print(row)
                movies.insert({'RatingID': row[0], 'Tag': row[1], 'Timestamp': row[2]})
    
    return movies
  
def findTag(param,movies):
    my_list=[]
    for doc in movies.find({"RatingID" : param}):
        #print (doc)
        #print (doc['MovieID'], doc['Tag'])
        my_list.append(doc['Tag'])    
    return my_list
        
