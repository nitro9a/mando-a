from typing import List, Tuple
from utils.database_connection import DatabaseConnection

Word = Tuple[str, str, str]

def access_word_table(database) -> List[Word]:
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Mando_a')
        words = cursor.fetchall()
    return words

def mark_as_read(database, Mandoa):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE Mando_a SET read=1 WHERE Mandoa=?', (str(Mandoa),))

def remove_word(database, Mandoa):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Mando_a WHERE Mandoa=?', (str(Mandoa),))

def add_word(database, Mandoa, Pronunciation, English, Read):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Mando_a VALUES (?,?,?,?)', (Mandoa, Pronunciation, English, Read))

