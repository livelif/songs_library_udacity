# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("""
create table if not exists songplays 
(
songplay_id serial PRIMARY KEY, 
start_time timestamp not null, 
user_id int, 
level varchar, 
song_id varchar, 
artist_id varchar, 
session_id varchar, 
location varchar, 
user_agent varchar)
""")

user_table_create = ("""
create table if not exists users (
user_id int PRIMARY KEY NOT NULL, 
first_name varchar, 
last_name varchar, 
gender varchar, 
level varchar
);
""")

song_table_create = ("""
create table if not exists songs (
song_id varchar PRIMARY KEY NOT NULL, 
title varchar, 
artist_id varchar, 
year int, 
duration double precision);
""")

artist_table_create = ("""
create table if not exists artists (
artist_id varchar PRIMARY KEY NOT NULL, 
name varchar, 
location varchar, 
latitude varchar, 
longitude varchar);
""")

time_table_create = ("""
create table if not exists time (
start_time TIMESTAMP PRIMARY KEY NOT NULL, 
hour int, 
day int, 
week int, 
month varchar, 
year int, 
weekday varchar);
""")

# INSERT RECORDS

songplay_table_insert = ("""
    insert into songplays 
    (
        start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
    ) 
    values (TO_TIMESTAMP(%s / 1000.0), %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    insert into users 
    (
        user_id, first_name, last_name, gender, level
    ) 
    values(%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
    DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""
    insert into songs 
    (
        song_id, title, artist_id, year, duration
    ) 
    values(%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
    insert into artists 
    (
        artist_id, name, location, latitude, longitude
    ) 
    values(%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id)
    DO UPDATE SET artist_id = EXCLUDED.artist_id || 'keyDuplicate';
""")


time_table_insert = ("""
    insert into time 
    (
        start_time, hour, day, week, month, year, weekday
    ) 
    values(TO_TIMESTAMP(%s / 1000.0), %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time)
    DO NOTHING;
""")

# FIND SONGS

song_select = ("""select distinct s.song_id, s.artist_id from songs s inner join artists t on s.artist_id = t.artist_id where s.title = %s and t.name = %s and s.duration = %s""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]