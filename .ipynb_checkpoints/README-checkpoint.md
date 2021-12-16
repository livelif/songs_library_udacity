#Project description
This project is about a music store where we get the raw data and make transformations.

#Database Design
We will use a star schema model.

##Fact Tables
Songplay: Store data about the sells

##Dimension Tables
Artists: Store data about artists
Songs: Store data about the songs and their artists
Users: Store data about the users of music store
Time: Calendar Dimension

#ETL Process
The steps:
1. Get the data from data/log_data and data/song_data
2. Get the most important values and create a pandas dataframe
3. Make some transformations
4. Execute SQL queries to insert the data in a postgres database

#Project Repository files

##data/log_data
Contains timestamp, user and songplay data

##data/song_data
Contains song and artists data

#How To Run the Project
1. Run python create_tables.py
2. Run python etl.py

![Star Schema](/Song_ERD.png "")