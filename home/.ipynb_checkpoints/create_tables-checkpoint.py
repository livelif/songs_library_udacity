import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    drop_table_queries = [
        "drop table if exists users",
        "drop table if exists songs",
        "drop table if exists artists",
        "drop table if exists time",
        "drop table if exists songplays"
    ]
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    
    create_table_queries = [
        """create table if not exists songplays 
            (
                songplay_id serial PRIMARY KEY, 
                start_time timestamp not null, 
                user_id int, 
                level varchar, 
                song_id varchar, 
                artist_id varchar, 
                session_id varchar, 
                location varchar, 
                user_agent varchar
            );""",
        """
        create table if not exists users 
            (
                user_id int PRIMARY KEY NOT NULL, 
                first_name varchar, 
                last_name varchar, 
                gender varchar, 
                level varchar
            );
            """,
            """
            create table if not exists songs 
                (
                    song_id varchar PRIMARY KEY NOT NULL, 
                    title varchar, 
                    artist_id varchar, 
                    year int, 
                    duration double precision
                );
            """,
            """
            create table if not exists artists 
                (
                    artist_id varchar PRIMARY KEY NOT NULL, 
                    name varchar, 
                    location varchar, 
                    latitude varchar, 
                    longitude varchar
                );
            """,
            """
            create table if not exists time 
                (
                    start_time TIMESTAMP PRIMARY KEY NOT NULL, 
                    hour int, 
                    day int, 
                    week int, 
                    month varchar, 
                    year int, 
                    weekday varchar
                );
            """
    ]
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()