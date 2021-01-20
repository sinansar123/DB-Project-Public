#currently creates empty tables for the whole database.
import psycopg2
import os
import sys
con = psycopg2.connect(database="findyourtone", user="postgres", password="qweqweqwe", host="127.0.0.1", port="5432")

print("Database opened successfully")

cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS USERS(
    Id serial,
    Name varchar NOT NULL,
    Username varchar NOT NULL UNIQUE,
    Password varchar NOT NULL,
    Location varchar,  
    About text, 
    genre varchar, 
    Category int DEFAULT 0,
    Reg_date date DEFAULT CURRENT_DATE, 
    PRIMARY KEY(Id));''')

cur.execute(''' 
    CREATE TABLE IF NOT EXISTS ARTIST(
    Id serial , 
    band varchar, 
    label varchar,
    FOREIGN KEY (Id) REFERENCES Users(Id) ON DELETE CASCADE);''')
print("Table created successfully")

cur.execute('''
    CREATE TABLE IF NOT EXISTS ADMINISTRATOR(
    Id serial,
    email varchar , 
    phone varchar, 
    section varchar,
    FOREIGN KEY (Id) REFERENCES USERS(Id) ON DELETE CASCADE);
    ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS INSTRUMENTS(
    Id serial,
    type varchar , 
    model varchar, 
    prod_year int,
    mods text,
    link varchar,
    added_by integer,
    PRIMARY KEY(Id),
    FOREIGN KEY (added_by) REFERENCES USERS(Id) ON DELETE CASCADE);
    ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS AMPS(
    Id serial,
    model varchar , 
    brand varchar, 
    prod_year int,
    watts float,
    tubes varchar,
    mic varchar,
    link varchar,
    added_by int,
    PRIMARY KEY(Id),
    FOREIGN KEY (added_by) REFERENCES USERS(Id) ON DELETE CASCADE);
    ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS SONGS(
    song_Id serial,
    name varchar , 
    album varchar, 
    release_date int,
    label varchar,
    artist_id integer,
    PRIMARY KEY(song_Id),
    FOREIGN KEY (artist_id) REFERENCES USERS(Id) ON DELETE CASCADE);
    ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS SETTINGS(
    Id serial,
    bass float , 
    mid float ,
    treble float,
    volume float ,
    master float ,
    gain float ,
    presence float ,
    spec_eq float ,
    effects text,
    genre   varchar,
    added_by integer,
    PRIMARY KEY(Id),
    FOREIGN KEY (added_by) REFERENCES USERS(Id) ON DELETE CASCADE);
    ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS SOUNDS(
    sound_Id serial,
    name varchar , 
    user_id integer, 
    genre varchar, 
    amp_id integer, 
    instrument_id integer,
    setting_id integer,
    descript text,
    sample varchar,
    song_id integer,
    up_date date DEFAULT CURRENT_DATE, 
    PRIMARY KEY(sound_Id),
    FOREIGN KEY (user_id) REFERENCES USERS(Id) ON DELETE CASCADE,
    FOREIGN KEY (instrument_id) REFERENCES INSTRUMENTS(Id) ON DELETE CASCADE,
    FOREIGN KEY (amp_id) REFERENCES AMPS(Id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES SONGS(song_id) ON DELETE CASCADE,
    FOREIGN KEY (setting_id) REFERENCES SETTINGS(Id) ON DELETE CASCADE);
''')

con.commit()
con.close()
