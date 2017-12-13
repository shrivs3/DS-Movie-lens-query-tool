import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import pandas as pd
from mongofile import *

# Class where all the functions of the project reside.
class MovieData:

     # Constructor function which creates creates the connection with the database 'finalproject'. 
     # If the database and user do not exist, then this function will create:
     # --> new user: 'finalproject'
     # --> password: 'finalproject'
     # --> database: 'finalproject'

     # During the set up, it is required to enter the super ux`sername and password for postgres. It is required that the user have a default database
     # called 'postgres' which is created during installation of postgres on a machine by default.

     # ALternatively, you can also manually enter the username, password and database name in the code in line 35 and comment out lines 28-31.
     def __init__(self, connection_string):  
          
          try:
               check()
               self.conn = psycopg2.connect(connection_string)
               self.mongo= initMongo()
               check()
          except:
               
               print("\n\n=========================================  INSTALLATION  ========================================")
               print("This is a one time installation. Please read the instructions carefully and enter the following data.\n\n")
               # COMMENT BEGIN
               print("Please enter postgres username:")
               username=raw_input()
               print("password:")
               password=raw_input()
               # COMMENT END

               # --> Manually enter database details here.
               con = psycopg2.connect(dbname='postgres',user=username, host = 'localhost', password=password)
               
               print ("\n\n\n\nCreating Database...")
               # try:
               #      # output = subprocess.check_output(['psql','-c',"\"create user finalproject1;\""])
               #      output = subprocess.check_output(['psql','-U',username])
               # except subprocess.CalledProcessError as e:
               #      output = e.output
               #print subprocess.check_output(["createdb","-O","finalproject1","finalproject1",";"])
               # print subprocess.check_output(["GRANT","ALL","PRIVILEGES","ON","DATABASE","finalproject1","to","finalproject1",";"])
               # print subprocess.check_output(["\l"])
               # self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
               # cur = con.cursor()
               # cur.execute("CREATE DATABASE %s  ;" % self.db_name)
               con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
               cursor = con.cursor()
               cursor.execute("create user finalproject1 with password 'finalproject1';")
               cursor.execute("create database finalproject1;")
               cursor.execute("GRANT ALL PRIVILEGES ON DATABASE finalproject1 to finalproject1;")
               cursor.close()
               con.close()
               print ("Creating Tables...")
               # try:
               #      output = subprocess.check_output(["psql","-U finalproject1","-d finalproject1","-f"])
               # except subprocess.CalledProcessError as e:
               #      output = e.output
               #print "COPIED CSV TO DATABASE !!"
               self.conn = psycopg2.connect(connection_string)
               cursor = self.conn.cursor()
               self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
               cursor.execute("create table ratings (ratingId varchar, userId varchar,movieId varchar,rating float,timestamp double precision);")
               # cursor.execute("copy ratings from 'C:\Users\l\Google Drive\RPI Semester 3\Database Systems\Final Project\ratings.csv' DELIMITERS ',' CSV;")
               # print ("DONE!")
               cursor.execute("create table movies (movieId varchar, name varchar, year double precision,Mystery boolean,Drama boolean,Western boolean,SciFi \
                         boolean,Horror boolean,FilmNoir boolean,Crime boolean,Romance boolean,Fantasy boolean,Musical boolean,Animation boolean,War boolean,\
                         Adventure boolean,Action boolean,noGenre boolean,Comedy boolean,Documentary boolean,Children boolean,Thriller boolean,IMAX boolean);")
               # cursor.execute("copy movies from 'C:\Users\l\Google Drive\RPI Semester 3\Database Systems\Final Project\movies.csv' DELIMITERS ',' CSV;")
               # print ("DONE!")
               cursor.execute("GRANT ALL ON TABLE public.movies TO finalproject1;")
               cursor.execute("GRANT ALL ON TABLE public.ratings TO finalproject1;")
               print("Inserting data into tables...")
               self.insertData()
               print("Connecting with MongoDB...")
               self.mongo= initMongo()

               print("Setup Complete!\n\nPress enter to begin...")
               raw_input()

     def insertData(self):
          
          cursor = self.conn.cursor()
          self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
          movies=pd.read_csv("movies.csv")
          ratings=pd.read_csv("ratings.csv")


          for i in range(len(movies)):
               tup='' 
               for j in movies:
                    if j=='movieId' or j=='name':
                         a=str(movies[j][i])
                         a=a.replace('\'','\'\'')
                         tup+="'"+str(a)+"',"
                    else:
                         tup+=(str(movies[j][i])+',')
               #print tup
               cursor.execute("INSERT INTO movies VALUES("+tup[:-1]+")")
          print ("Just a few more seconds...")
          for i in range(len(ratings)):
               tup='' 
               for j in ratings:
                    if j in ["ratingId, userId,movieId"]:
                         tup+="'"+str(ratings[j][i])+"',"
                    else:
                         tup+=(str(ratings[j][i])+',')
               #print tup
               cursor.execute("INSERT INTO ratings VALUES("+tup[:-1]+")")
 

     def check_connectivity(self):
          cursor = self.conn.cursor()
          cursor.execute("SELECT * FROM movies LIMIT 1")
          records = cursor.fetchall()
          if len(records) == 1:
               print("...............................POSTGRES CONNECTIVITY ESTABLISHED!............................... \n\n\n\n\n\n")
          else:
               print("...............................POSTGRES CONNECTIVITY NOT ESTABLISHED!............................... \n\n\n\n\n\n")
          return
     
     def startUI(self):
          print ("-----------------------------------------------------------------------------------------------------------------------\n\n")
          print ("                                       WELCOME TO THE MOVIE RATINGS DATABASE PROJECT!           ")
          print ("                                         -by Shrey Shrivastava and Smit Pandit           \n\n")
          print ("-----------------------------------------------------------------------------------------------------------------------\n\n")
          print("  Please select one of the option you would like to use for EXPLORING the movie ratings!\n")
          print("1. Find Movies! \n2. Best/Worst movies \n3. Best/Worst Genres \n4. Popular Movies \n5. Popular Genres \n6. Find average ratings of any movie \
               \n7. Find tags for a given movie")
          print("--> to EXIT, write 'exit'\n")
          print("Please enter a number from 1-7 to select one of the above options:")
          
          return (raw_input())

     def selectOption(self, option1):
          
          flag=False
          if option1=='1':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 1. Find Movies \n\n"
          elif option1=='2':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 2. Best/Worst Movies\n\n"
          elif option1=='3':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 3. Best/Worst Genres\n\n"
          elif option1=='4':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 4. Popular Movies\n\n"
          elif option1=='5':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 5. Popular Genres\n\n"
          elif option1=='6':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 6. Find average rating for any movie\n\n"
          elif option1=='7':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nYou selected --> 7. Find tags for any movie\n\n"
          elif option1=='exit':
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print "\nPress Enter to exit. Thank you for visiting!!\n\n"
               raw_input()

          else:
               print ("\n\n---------------------------------------------------------------------------------------------\n\n")
               print ("\nPlease enter a valid number between 1-7. \n\n")
               flag=True
          
          return (flag)
     
     def findMovie(self):
          print ("\n---------------------------------------------------------------------------------------------\n")
          print ("Enter the information in the following format separated with commas:")
          print("-->Rating start value        -->Rating End Value          -->Year       ")
          print("      range:(0-5)                  range:(0-5)            (1902-2016)      \n")
          print ("-->Genres: Mystery, Drama, Western, SciFi, Horror, FilmNoir, Crime, Romance, Fantasy, Musical, Animation,\n          War, Adventure, Action, Comedy, Documentary, Children, Thriller, IMAX")
          print ("\n==>Example: 2.5, 4.5, 1999, crime\n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")
          print("Please enter the information in the format described above:\n")
          a= raw_input()
          if a=='exit':
               return
          try:
               rating_start, rating_end, year, genre= a.split(',')
     #          rating_start, rating_end=int(rating_start), int(rating_end)
               query="select movieid,name, ratings, year from movies natural join \
                    (select movieid,avg(rating) as ratings from ratings natural\
                     join movies group by movieid)avgratings where ratings<{} \
                     and ratings>{} and year=\'{}\' and {}=True order by ratings \
                     desc;".format(rating_end, rating_start, year, genre)
               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()
               #print records
               
               for i in records:
                    print("----------------\n"+"Movie: " +i[1])
                    print("Rating: "+str(i[2]))
                    print("Year: "+str(i[3]))

               print("\n Press enter to continue...\n\n\n")
               raw_input()
          except:
               self.conn.rollback()
               print("\n\n\n ERROR: The data you entered is not in the right format...\nPlease try again or write 'exit' to end.")
               self.findMovie()
          return

     
     def bestMovies(self):

          print ("\n---------------------------------------------------------------------------------------------\n")
          print ("\nPlease select one of the following: \n")
          print ("1. Best movies of all time (rated 5) ")
          print ("2. Best movies by year ")
          print ("3. Best movies by genre ")
          print ("4. Worst movies of all time ")
          print ("5. Worst movies by year ")
          print ("6. Worst movies by genre \n")
          print ("TO EXIT: write 'exit' \n")
          print ("\n---------------------------------------------------------------------------------------------\n")
          print (" Please enter a value from 1-6 ")
          option1=raw_input()

          if option1=='1':
               print("\n The Best Movies of All Time are:\n")
               query="select movieid,name, ratings, year\
                    from movies natural join (select movieid,avg(rating) \
                    as ratings from ratings natural join movies \
                    group by movieid)avgratings where ratings=5 \
                    order by ratings desc;"

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()

               a=0
               for i in records:
                    print(str(a)+". "+i[1]+" ("+str(int(i[3]))+")") 
                    a+=1          
               print("\n Press enter to continue...\n\n\n")
               raw_input()

               return     

          elif option1=='2':
               print ("_____________________________________________________________")
               print "You selected --> 2. Best Movies by Year (1902-2016)"
               print ("\nPlease enter the year:")
               year=raw_input()

               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where year='{}' order by ratings desc limit 10".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Best Movies of the year "+str(year)+" are:\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[2])+"/5)") 
                         a+=1          

                    print("\n Press enter to continue...\n\n\n")
                    raw_input()

               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.bestMovies()   
          
               return     

          elif option1=='3':
               print ("_____________________________________________________________")
               print "You selected --> 3. Best Movies by Genres"
               print ("\n\n-->Genres: Mystery, Drama, Western, SciFi, Horror, FilmNoir, Crime, Romance, Fantasy, Musical, Animation,\n          War, Adventure, Action, Comedy, Documentary, Children, Thriller, IMAX")

               print ("\nPlease enter the Genres:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where {}=True order by ratings desc limit 15".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Best Movies in "+str(year)+" genre are\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[3])+")"+" ("+str(i[2])+"/5)") 
                         a+=1          
                    
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.bestMovies()   


               return     

          if option1=='4':
               print("\n The Worst Movies of All Time are:\n")
               query="select movieid,name, ratings, year\
                    from movies natural join (select movieid,avg(rating) \
                    as ratings from ratings natural join movies \
                    group by movieid)avgratings where ratings<1 \
                    order by ratings;"

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()

               a=0
               for i in records:
                    print(str(a)+". "+i[1]+" ("+str(i[3])+")") 
                    a+=1          

               print("\n Press enter to continue...\n\n\n")
               raw_input()
               return     

          elif option1=='5':
               print ("_____________________________________________________________")
               print "You selected --> 5. Worst Movies by Year (1902-2016)"
               print ("\nPlease enter the year:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where year='{}' order by ratings limit 10".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Worst Movies of the year "+str(year)+" are:\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[2])+"/5)") 
                         a+=1          

                    print("\n Press enter to continue...\n\n\n")
                    raw_input()               
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.bestMovies()   
   
               return     

          elif option1=='6':
               print ("_____________________________________________________________")
               print "You selected --> 6. Worst Movies by Genres"
               print ("\n\n-->Genres: Mystery, Drama, Western, SciFi, Horror, FilmNoir, Crime, Romance, Fantasy, Musical, Animation,\n          War, Adventure, Action, Comedy, Documentary, Children, Thriller, IMAX")

               print ("\nPlease enter the Genre:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where {}=True order by ratings limit 15".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Worst Movies in "+str(year)+" genre are\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[3])+")"+" ("+str(i[2])+"/5)") 
                         a+=1          
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()  
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.bestMovies()   
   
               return     
          
          elif option1=='exit':
               return
          
          else:
               print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
               raw_input()
               self.bestMovies()


     def bestGenres(self):
          print ("\n---------------------------------------------------------------------------------------------\n")

          print ("\nPlease select one of the following: \n")
          print ("1. Best Genre of all time (rated 5) ")
          print ("2. Best Genre by year \n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")
          print (" Please enter a value from 1-2 ")
          option1=raw_input()

          if option1=='1':
               print ("_____________________________________________________________")
               print "You selected --> 1. Best Genre of all time (rated 5) "

               genre_list=['Mystery','Drama', 'Western' ,'SciFi','Horror' ,'FilmNoir' ,'Crime','Romance',\
               'Fantasy','Musical' ,'Animation','War','Adventure','Action','noGenre','Comedy ','Documentary','Children','Thriller','IMAX']
               
               genre_score=[]

               for i in genre_list:
                    query="select avg(ratings) from movies natural join (select movieid,avg(rating) as ratings from ratings \
                        natural join movies group by movieid)avgratings where {}=True".format(i);
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()
                    genre_score.append((records[0][0]))

               genre_score=[(x,y) for y,x in reversed(sorted(zip(genre_score,genre_list)))]

               a=1
               print ("\nThe Best Genres of all time are:")
               print ("\nGENRE NAME :: AVG RATING\n")
               for i in genre_score:
                    print (str(a)+". "+i[0]+":: "+str(i[1]))
                    a+=1

               print("\n**'noGenre' --> Genre data for movie missing **")
               print("\n Press enter to continue...\n\n\n")
               raw_input()     
               return

          elif option1=='2':

               print ("\n Please enter the year (1902-2016):")
               year=raw_input()
               genre_list=['Mystery','Drama', 'Western' ,'SciFi','Horror' ,'FilmNoir' ,'Crime','Romance',\
               'Fantasy','Musical' ,'Animation','War','Adventure','Action','noGenre','Comedy ','Documentary','Children','Thriller','IMAX']
               
               genre_score=[]
               try:
                    for i in genre_list:
                         query="select avg(ratings) from movies natural join (select movieid,avg(rating) as ratings from ratings \
                             natural join movies group by movieid)avgratings where year={} and {}=True".format(year, i);
                         cursor = self.conn.cursor()
                         cursor.execute(query)
                         records = cursor.fetchall()
                         genre_score.append((records[0][0]))

                    genre_score=[(x,y) for y,x in reversed(sorted(zip(genre_score,genre_list)))]

                    a=1
                    print ("\nThe Best Genres of the year "+str(year)+" are:")
                    print ("\nGENRE NAME :: AVG RATING\n")
                    for i in genre_score:
                         print (str(a)+". "+i[0]+":: "+str(i[1]))
                         a+=1
                    print("\n**'noGenre' --> Genre data for movie missing **")
                    print("\n Press enter to continue...\n\n\n")
                    raw_input() 
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.bestGenres()   

          elif option1=='exit':
               return

          else:
               print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
               raw_input()
               self.bestGenres()    
          return
          
     def popularMovies(self):

          print ("\n---------------------------------------------------------------------------------------------\n")
          print ("\nPlease select one of the following: \n")
          print ("1. Most Popular movies of all time ")
          print ("2. Most Popular movies by year ")
          print ("3. Most Popular movies by genre ")
          print ("4. Least Popular movies of all time ")
          print ("5. Least Popular movies by year ")
          print ("6. Least Popular movies by genre \n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")
          option1=raw_input()

          if option1=='1':
               print("\n The Most Popular Movies of All Time are:\n")
               query="select movieid,name, ratings, year\
                    from movies natural join (select movieid,avg(rating) \
                    as ratings from ratings natural join movies \
                    group by movieid)avgratings where ratings=5 \
                    order by ratings desc;"

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()

               a=0
               for i in records:
                    print(str(a)+". "+i[1]+" ("+str(i[3])+")") 
                    a+=1          
               print("\n Press enter to continue...\n\n\n")
               raw_input()     
               return     

          elif option1=='2':
               print ("_____________________________________________________________")
               print "You selected --> 2. Most Popular Movies by Year (1902-2016)"
               print ("\nPlease enter the year:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where year='{}' order by ratings desc limit 10".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Most Popular Movies of the year "+str(year)+" are:\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[2])+"/5)") 
                         a+=1          
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()     
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.popularMovies()   
               return     

          elif option1=='3':
               print ("_____________________________________________________________")
               print "You selected --> 3. Most Popular Movies by Genres"
               print ("\n\n-->Genres: Mystery, Drama, Western, SciFi, Horror, FilmNoir, Crime, Romance, Fantasy, Musical, Animation,\n          War, Adventure, Action, Comedy, Documentary, Children, Thriller, IMAX")

               print ("\nPlease enter the Genres:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where {}=True order by ratings desc limit 15".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Most Popular Movies in "+str(year)+" genre are\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[3])+")"+" ("+str(i[2])+"/5)") 
                         a+=1          
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()     
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.popularMovies()
               return     

          if option1=='4':
               print("\n The Least Popular Movies of All Time are:\n")
               query="select movieid,name, ratings, year\
                    from movies natural join (select movieid,avg(rating) \
                    as ratings from ratings natural join movies \
                    group by movieid)avgratings where ratings<1 \
                    order by ratings;"

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()

               a=0
               for i in records:
                    print(str(a)+". "+i[1]+" ("+str(i[3])+")") 
                    a+=1          
               print("\n Press enter to continue...\n\n\n")
               raw_input()     
               return     

          elif option1=='5':
               print ("_____________________________________________________________")
               print "You selected --> 5. Least Popular Movies by Year (1902-2016)"

               print ("\nPlease enter the year:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where year='{}' order by ratings limit 10".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Least Popular Movies of the year "+str(year)+" are:\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[2])+"/5)") 
                         a+=1          
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()     
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.popularMovies()
               return     

          elif option1=='6':
               print ("_____________________________________________________________")
               print "You selected --> 6. Least Popular Movies by Genres"
               print ("\n\n-->Genres: Mystery, Drama, Western, SciFi, Horror, FilmNoir, Crime, Romance, Fantasy, Musical, Animation,\n          War, Adventure, Action, Comedy, Documentary, Children, Thriller, IMAX")

               print ("\nPlease enter the Genre:")
               year=raw_input()
               try:
                    query=" select movieid,name, ratings, year from movies natural join (select movieid,avg(rating) as ratings \
                         from ratings natural join movies group by movieid)avgratings where {}=True order by ratings limit 15".format(year);
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()

                    a=0
                    print ("\nThe Least Popular Movies in "+str(year)+" genre are\n")
                    for i in records:
                         print(str(a)+". "+i[1]+" ("+str(i[3])+")"+" ("+str(i[2])+"/5)") 
                         a+=1          
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()     
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.popularMovies()
               return    

          elif option1=='exit':
               return
          
          else:
               print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
               raw_input()
               self.popularMovies() 
          
     def popularGenres(self):
          print ("\n---------------------------------------------------------------------------------------------\n")
          print ("\nPlease select one of the following: \n")
          print ("1. Most Popular Genre of all time (rated 5) ")
          print ("2. Most Popular by year \n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")

          print (" Please enter a value from 1-2 ")
          option1=raw_input()

          if option1=='1':
               print ("_____________________________________________________________")
               print "You selected --> 1. Most Popular Genre of all time (rated 5) "

               genre_list=['Mystery','Drama', 'Western' ,'SciFi','Horror' ,'FilmNoir' ,'Crime','Romance',\
               'Fantasy','Musical' ,'Animation','War','Adventure','Action','noGenre','Comedy ','Documentary','Children','Thriller','IMAX']
               
               genre_score=[]

               for i in genre_list:
                    query="select sum(ratings) from movies natural join (select movieid, count(rating) as ratings from ratings \
                        natural join movies group by movieid)avgratings where {}=True".format(i);
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()
                    genre_score.append((records[0][0]))

               genre_score=[(x,y) for y,x in reversed(sorted(zip(genre_score,genre_list)))]

               a=1
               print ("\nThe Most Popular Genres of all time are:")
               print ("\n GENRE NAME :: \n")
               for i in genre_score:
                    print (str(a)+". "+i[0])
                    a+=1

               print("\n**'noGenre' --> Genre data for movie missing **")
               print("\n Press enter to continue...\n\n\n")
               raw_input()     

          elif option1=='2':

               print ("\n Please enter the year (1902-2016):")
               year=raw_input()
               genre_list=['Mystery','Drama', 'Western' ,'SciFi','Horror' ,'FilmNoir' ,'Crime','Romance',\
               'Fantasy','Musical' ,'Animation','War','Adventure','Action','noGenre','Comedy ','Documentary','Children','Thriller','IMAX']
               
               genre_score=[]
               try:
                    for i in genre_list:
                         query="select sum(ratings) from movies natural join (select movieid,count(rating) as ratings from ratings \
                             natural join movies group by movieid)avgratings where year={} and {}=True".format(year, i);
                         cursor = self.conn.cursor()
                         cursor.execute(query)
                         records = cursor.fetchall()
                         genre_score.append((records[0][0]))


                    genre_score=[(x,y) for y,x in reversed(sorted(zip(genre_score,genre_list)))]

                    a=1
                    print ("\nThe Most Popular Genres for the year "+str(year)+" are:")
                    print ("\n GENRE NAME :: \n")
                    for i in genre_score:
                         print (str(a)+". "+i[0])
                         a+=1
                    print("\n**'noGenre' --> Genre data for movie missing **")
                    print("\n Press enter to continue...\n\n\n")
                    raw_input() 
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.popularGenres()

          elif option1=='exit':
               return
          else:
               print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
               raw_input()
               self.popularGenres()                  
          return
          
          
     def findRating(self):
          print ("\n---------------------------------------------------------------------------------------------\n")
          print("\nPlease enter the name of the movie:")
          print ("--> To see the list of movies, please write 'movies'")
          print ("--> For example: 'Inception', 'Crash', 'movies' \n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")
          
          movies=raw_input()
#          rating_start, rating_end=int(rating_start), int(rating_end)

          if movies=='movies':
               print("\nPlease enter the year:")
               year=raw_input()
               query="select name from movies where year={};".format(year)

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()
               #print records
               
               for i in records:
                    print(i[0])

               print("\n TOTAL RECORDS FOUND: "+str(len(records)))
               print("\n Press enter to continue...\n\n\n")
               raw_input()     
               self.findRating() 

          elif movies=='exit':
               return
          else: 
               try:
                    query="select movieid, name, ratings, year from movies natural join (select movieid,avg(rating) as ratings from ratings \
                             natural join movies group by movieid)avgratings where name=\'{}\';".format(movies)

                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()
                    #print records
                    
                    for i in records:
                         print("----------------\n"+"Movie: " +i[1])
                         print("Rating: "+str(i[2]))
                         print("Year: "+str(i[3]))
                    print("\n Press enter to continue...\n\n\n")
                    raw_input()
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.findRating() 
          return

     def findTag(self):
          print ("\n---------------------------------------------------------------------------------------------\n")
          print("\nPlease enter the name of the movie:")
          print ("--> To see the list of movies, please write 'movies'")
          print ("--> For example: 'Toy Story, 'movies' \n")
          print ("(To exit, write 'exit')")
          print ("\n---------------------------------------------------------------------------------------------\n")
          
          movies=raw_input()
#          rating_start, rating_end=int(rating_start), int(rating_end)

          if movies=='movies':
               print("\nPlease enter the year:")
               year=raw_input()
               query="select name from movies where year={};".format(year)

               #print query
               cursor = self.conn.cursor()
               cursor.execute(query)
               records = cursor.fetchall()
               #print records
               
               for i in records:
                    print(i[0])

               print("\n TOTAL RECORDS FOUND: "+str(len(records)))
               print("\n Press enter to continue...\n\n\n")
               raw_input()     
               self.findRating() 

          elif movies=='exit':
               return

          else:
               try:
                    query="select distinct(ratingid), name, year from ratings natural join movies where name=\'{}\' order by year;".format(movies)
                    #print query
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    records = cursor.fetchall()
                    
                    print ("Tags: ")
                    tags_bool=False               
                    for i in records:
                         # print("----------------\n"+"Movie: " +i[1])
                         # print("Year: "+str(i[2]))
                         input_str=i[0]
                         #print input_str
                         tag_list = findTag(input_str,self.mongo)
                         #print type(tag_list)
                         if tag_list==[]:
                              continue;
                         else:
                              for tag in list(set(tag_list)):
                                   print ("--> "+tag)
                              tags_bool=True

                    if tags_bool==False:
                         print("No tags found. Search another movie..")
                         self.findTag()

                    print("\n Press enter to continue...\n\n\n")
                    raw_input()     
               except:
                    self.conn.rollback()
                    print ("\n ERROR: Invalid option selected. Please press 'enter'..\n ")
                    raw_input()
                    self.findTag() 

          return



if __name__ == '__main__':
     connection_string = "host='localhost' dbname='finalproject1' user='finalproject1' password='finalproject1'"
     a=MovieData(connection_string)
     a.check_connectivity() 
     run=True
     while (run):
          option1=a.startUI()
          flag1=a.selectOption(option1)
          while flag1:
               option1=raw_input()
               flag1= a.selectOption(option1)
          
          if option1=='1':
               a.findMovie()
          elif option1=='2':
               a.bestMovies()          
          elif option1=='3':
               a.bestGenres()
          elif option1=='4':
               a.popularMovies()
          elif option1=='5':
               a.popularGenres()
          elif option1=='6':
               a.findRating()
          elif option1=='7':
               a.findTag()
          elif option1=='exit':
               run=False


          
     
     
     
     