import sqlite3
import random
from utils import database
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
word_dict = {}

white = (1,1,1,1)
black = (0,0,0,0)
yellow = (.9, .8, 0, 1)
red = (.9, .3, 0, 1)
orange = (.9, .5, 0, 1)

class appLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(appLayout, self).__init__(**kwargs)
        self.button= Button(text= 'Click Here', font_size = 30, color = yellow, pos_hint = {'center_x': 0.5, 'center_y': .8}, size_hint = (.25, .25))
        self.label = Label(text = '')
        self.button.bind(on_press = self.random_word)
        self.add_widget(self.button)
        self.add_widget(self.label)

    def random_word(self, event):

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
        self.label.text = (f'Word: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')

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


class WordApp(App):

    def build(self):
        appL = appLayout()
        return appL

if __name__=="__main__":
    WordApp().run()





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

