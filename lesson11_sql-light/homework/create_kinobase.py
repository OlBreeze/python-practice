import sqlite3
conn = sqlite3.connect('kinobase.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     release_year INTEGER NOT NULL,
                     genre TEXT NOT NULL )
                                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS actors
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     birth_year INTEGER NOT NULL )
                                ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS movie_cast
                    (movie_id INTEGER NOT NULL,
                    actor_id INTEGER NOT NULL,
                    PRIMARY KEY (movie_id, actor_id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
                    FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE)
                                ''')

conn.commit()