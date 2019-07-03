import sqlite3
import random
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

        #get a word from the unread table
        get_words(database.access_word_table('mando-a_unread.db'))

        #mark as read in the all table
        random_w = random.choice(word_dict)
        database.mark_as_read('mando-a_all.db', str(random_w['Word']))

        #random_w is the entire dictionary entry - I need to access just the 'Word' portion
        word = (str(random_w['Word']))
        pro = (str(random_w['Pronunciation']))
        eng =  (str(random_w['English']))
        print (str(random_w['Word']))
        self.translation.text = (f'Word: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')
        #TODO look at exercise dice, gen_ex_die, for line in text - figure out text wrapping
        #remove fetched word from the unread table
        database.remove_word('mando-a_unread.db', str(random_w['Word']))

        #add fetched word to the read table
        database.add_word('mando-a_read.db', random_w['Word'], random_w['Pronunciation'], random_w['English'], Read=1)


def get_words(database):
    count = 0
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



    #TODO Find out what happens when all words are removed
    #TODO Make pages
    #TODO Create a new list of unread words, 'remove word' from 'unread word' list - FINISHED
    #TODO Add random word to a 'read words' list - FINISHED
    #TODO Add reset
    #TODO Add ability to favorite
    #TODO Edit database to have only unique entries
    #TODO Add what happens when there are no words left

'''
https://stackoverflow.com/questions/38353957/output-text-in-kivy
'''

#random_word()

