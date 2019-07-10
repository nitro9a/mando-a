import sqlite3
import random
import textwrap
import mando_a
from utils import database, scalelabel, scrollablelabel
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty


word_dict = {}

white = (1,1,1,1)
black = (0,0,0,0)
yellow = (.9, .8, 0, 1)
red = (.9, .3, 0, 1)
orange = (.9, .5, 0, 1)

class ReadWords(Screen):
    pass

class Favorites(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class WordADay(Screen):
    get = ObjectProperty(None)
    translation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WordADay, self).__init__(**kwargs)

    def random_word(self):
        con = sqlite3.connect('mando-a_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT * from Mando_a")
        rowcount = len(cursor.fetchall())

        def get_words(database):
            count = -1
            for word in database:

                count += 1

                entry = {
                    count : {
                        'Word': word[0],
                        'Pronunciation': word[1],
                        'English': word[2],
                        'Read': word[3]
                }
                }

                word_dict.update(entry)

        def get_random_word():
            #get words from the unread table and add them to word_dict using function "get_words"
            get_words(database.access_word_table('mando-a_unread.db'))

            #get a row from word_dict

            try:
                #get a row from word_dict
                random_w = random.choice(word_dict)

                #random_w is the entire dictionary entry - I need to access just the 'Word' portion
                word = (str(random_w['Word']))
                pro = (str(random_w['Pronunciation']))
                eng =  (str(random_w['English']))
                print (str(random_w['Word']))

                text_result = (f'\n\nWord: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')

                self.translation.text = text_result

                #mark as read in the all table
                database.mark_as_read('mando-a_all.db', str(random_w['Word']))

                #remove fetched word from the unread table
                database.remove_word('mando-a_unread.db', str(random_w['Word']))

                #add fetched word to the read table
                database.add_word('mando-a_read.db', random_w['Word'], random_w['Pronunciation'], random_w['English'], Read=1)

                word_dict.clear()

            except KeyError:
                print("key error")

        if rowcount == 0:
            print("finished")
        elif rowcount >= 1:
            get_random_word()

class UnreadWords(Screen):

    unread_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    entry = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UnreadWords, self).__init__(**kwargs)

    def reset_databases(self):

        mando_a.delete_database_all('mando-a_all.db')
        mando_a.delete_database_unread('mando-a_unread.db')
        mando_a.delete_database_read('mando-a_read.db')

        mando_a.create_database('mando-a.csv', 'mando-a_all.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

        mando_a.create_database('mando-a.csv', 'mando-a_unread.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

        mando_a.create_database('mando-a_read.csv', 'mando-a_read.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

    def display_database(self):
        text_result = str(random.randint(1,100))
        self.unread_table.text = text_result

kv = Builder.load_file("layout.kv")

class WordApp(App):
    def build(self):
        return kv

if __name__=="__main__":
    WordApp().run()




    #TODO look at exercise dice, gen_ex_die, for line in text - figure out text wrapping - FINISHED
    #TODO Make pages - FINISHED
    #TODO Create a new list of unread words, 'remove word' from 'unread word' list - FINISHED
    #TODO Add random word to a 'read words' list - FINISHED
    #TODO Figure out why program is crashing seemingly randomly on random choice - FINISHED
    #TODO Add reset - FINISHED
    #TODO Figure out how to make page navigation buttons uniform even when the rest of the layout is different (it works,
    # continued... if you use the same amount of layouts no matter their size.  Can probably adjust padding for
    # different number of layouts - FINISHED
    #TODO Add table with scrolling text results
    #TODO Page 2
    #TODO Page 3
    #TODO Page 4
    #TODO Add ability to favorite
    #TODO Edit database to have only unique entries
    #TODO Add what happens when there are no words left
    #TODO Notifications
    #TODO Limit length of entries?
    #TODO Make pretty
    #TODO Add touch events

'''
https://stackoverflow.com/questions/38353957/output-text-in-kivy
'''

