'''Creates database'''

import sqlite3
import csv

def create_database(csv_file, database, execute_create, execute_insert):
    f = open(csv_file,'r')
    next(f, None)
    reader = csv.reader(f)

    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute(execute_create)

    for row in reader:
        cursor.execute(execute_insert, row)

    f.close()
    sql.commit()
    sql.close()

def delete_database_all(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Mando_a")

def delete_database_unread(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Mando_a")

def delete_database_read(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Mando_a")

create_database('mando-a-short.csv', 'mando-a_all.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

create_database('mando-a-short.csv', 'mando-a_unread.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

create_database('mando-a_read.csv', 'mando-a_read.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")