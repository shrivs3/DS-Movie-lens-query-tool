# Database Final Project
##     -Shrey Shrivastava and Smit Pandit

## 1)	What data you used and where you got it?
->	The data was from the MovieLens 100K dataset and its size was 5 mb. The data is present at the Grouplens website. The dataset consisted of three files Rating.dat, Tags.dat and Movies.dat. These were converted into CSV files for ease in loading into PostgreSQL database and MongoDB database. The Tags.csv and Ratings.csv had ratingId, userId and movieId fields in common. So for the purposes of normalization userId and movieId fields were removed from Tags.csv.

## 2)	How to build your application?
->	We will be providing both the executable file to run the code and the python script that contains the code. You can run the python script, from the python interface on command prompt or an IDE of your choice, to use the application. However, there are a few libraries that need to be installed in the system before running the code. They are:<br/>
i.	psycopg2<br/>
ii.	pandas<br/>
iii.	pymongo<br/>
All of these libraries can be installed by using the “pip install <library-name>” command on the command prompt.<br/>
Also ensure that all the csv files and the executable file/python script are in the same directory

## 3)	How to load the data into your application?
->	The python script automatically loads the data into the PostgreSQL and MongoDB databases. However, there a few steps that need to be followed to ensure that the data gets loaded:<br/>
i.	Make sure PostgreSQL is running<br/>
ii.	Download and install MongoDB if it isn’t present in the system (https://www.mongodb.com/download-center#community)<br/>
iii.	Once installed add the path of the ‘bin’ folder present in the newly installed MongoDB folder to the ‘Path’ Environment Variable of your computer.<br/>
iv.	Create a folder in the directory where you want to store the Mongo database.<br/>
v.	Open command prompt and type:<br/>
 mongod -dbpath "<directory-of-the-folder>" and let it run<br/>
vi.	Open another command prompt and enter “mongo” to see if MongoDB is running<br/>
vii.	Run the code or the executable. The application will do the rest.

## 4)	How to run and use the application to explore the data?
->	The application can be used by either running the executable file or the python script while ensuring that all the CSV files are in the same directory as the executable or the python script. The application asks for the username and password for the PostgreSQL at the beginning of execution. Then the application loads all the data into the respective PostgreSQL and MongoDB databases. Once that is done the user gets to interact with the Text based interface to explore the data. If you do not want to insert the username and password into the application you can hard code the details into the python script at line 38.<br/> The code is as follows:<br/>
<br/>
con = psycopg2.connect(dbname='postgres',user=username, host = 'localhost', password=password)<br/>
<br/>
Replace username and password with the actual username and password of PostgreSQL and when the application asks for username and password simply press ENTER both times to skip the step.
