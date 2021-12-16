import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from pandas.io.json import json_normalize
from pathlib import Path
import json
import uuid


def process_song_file(cur, filepath):
    """
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath
    """
    # open song file
    df = pd.read_json(filepath,lines = True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]]
    cur.execute(song_table_insert, song_data.values[0])
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]]
    cur.execute(artist_table_insert, artist_data.values[0])


def process_log_file(cur, filepath):
    """
    This procedure processes a log file whose filepath has been provided as an arugment.
    It extracts the log information in order to store it into the time table.
    After this it extracts user information in order to store it into the user table.
    Then it extracts the songplay information in order to store it into the songplay table.

    INPUTS: 
    * cur the cursor variable
    * filepath
    """
    # open log file

    df = pd.read_json(filepath,lines = True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"])
    
    # insert time data records
    time_data = list(zip(df.ts, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = ["timestamp", "hour", "day", "week", "month", "year", "weekday"]
    time_df = time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    cont = 0
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        cur.execute(songplay_table_insert, (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent))


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    #process_log_file(cur, '/home/workspace/data/log_data/2018/11/2018-11-30-events.json') its works... Udacity gives to me a corrupted files
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()