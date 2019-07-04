import sqlite3
import random
import textwrap
from utils import database, scalelabel
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

word_dict = {}

white = (1,1,1,1)
black = (0,0,0,0)
yellow = (.9, .8, 0, 1)
red = (.9, .3, 0, 1)
orange = (.9, .5, 0, 1)

class UnreadWords(Screen):
    pass

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
        self.label = Label(text = '')
        self.add_widget(self.label)

    def random_word(self):
        con = sqlite3.connect('mando-a_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT * from Mando_a")
        rowcount = len(cursor.fetchall())

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

                #self.translation.text = str(textwrap.wrap((f'Word: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}'), width = 6))
                text_result = (f'Word: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')
                #self.translation.text = '\n'.join(textwrap.wrap(text_result, width=40, replace_whitespace=False))
                self.translation.text = text_result
                #TODO look at exercise dice, gen_ex_die, for line in text - figure out text wrapping

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

kv = Builder.load_file("layout.kv")

class WordApp(App):
    def build(self):
        return kv

if __name__=="__main__":
    WordApp().run()


    #TODO Make pages
    #TODO Create a new list of unread words, 'remove word' from 'unread word' list - FINISHED
    #TODO Add random word to a 'read words' list - FINISHED
    #TODO Add reset
    #TODO Add ability to favorite
    #TODO Edit database to have only unique entries
    #TODO Add what happens when there are no words left
    #TODO Notifications
    #TODO Figure out why program is crashing seemingly randomly on random choice - FINISHED
    #TODO Limit length of entries?
    #TODO Make pretty

'''
https://stackoverflow.com/questions/38353957/output-text-in-kivy
'''

