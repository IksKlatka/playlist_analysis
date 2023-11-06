import sqlite3

connection = sqlite3.connect("current_user.sqlite")
cur = connection.cursor()

cur.execute(f"""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        user_id VARCHAR(40),
        username TEXT
    );
""")

cur.execute(f"""
    CREATE TABLE IF NOT EXISTS playlist (
        id SERIAL PRIMARY KEY, 
        playlist_id VARCHAR(40),
        name TEXT,
        total_songs INTEGER,
        duration INTEGER,
        date_created DATE    
    );
""")


cur.execute(f"""
    CREATE TABLE IF NOT EXISTS tracks (
        id SERIAL PRIMARY KEY, 
        track_id VARCHAR(40),
        name TEXT,
        artist TEXT,
        genre TEXT, 
        duration INTEGER,
        valence REAL
    );
""")

