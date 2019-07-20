import sqlite3
import csv
import random
import textwrap
from utils import database, scalelabel, scrollablelabel
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty

white = (1,1,1,1)
black = (0,0,0,0)
yellow = (.9, .8, 0, 1)
red = (.9, .3, 0, 1)
orange = (.9, .5, 0, 1)

class MessageBox(Popup):
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):
        super(MessageBox, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('unread').unread_dict[obj.text]
        self.obj_text = word_data[0] + '\n' + word_data[1] + '\n' + word_data[2]

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """

class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        #print(type(data))
        #print(f'Data: {data.items()}, Index: {index},rv: {rv}, Type: {type(data)}')
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def on_press(self):
        popup = MessageBox(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class RV(RecycleView):
    #data_items = ListProperty([])
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class Favorites(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class WordADay(Screen):

    word_dict = {}

    get = ObjectProperty(None)
    translation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WordADay, self).__init__(**kwargs)
        self.unread_dict = {}

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

                self.word_dict.update(entry)

        def get_random_word():
            #get words from the unread table and add them to word_dict using function "get_words"
            get_words(database.access_word_table('mando-a_unread.db'))

            #get a row from word_dict

            try:
                #get a row from word_dict
                random_w = random.choice(self.word_dict)

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

                self.word_dict.clear()


            except KeyError:
                print("key error")

        if rowcount == 0:
            print("finished")
        elif rowcount >= 1:
            get_random_word()

class UnreadWords(Screen):

    unread_dict = {}

    unread_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Mandoa", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(UnreadWords, self).__init__(**kwargs)
        self.unread_dict = {}

    def reset_databases(self):

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

        delete_database_all('mando-a_all.db')
        delete_database_unread('mando-a_unread.db')
        delete_database_read('mando-a_read.db')

        create_database('mando-a-short.csv', 'mando-a_all.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

        create_database('mando-a-short.csv', 'mando-a_unread.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

        create_database('mando-a-short.csv', 'mando-a_read.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

    def display_database(self):
        con = sqlite3.connect('mando-a_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT Mandoa, Pronunciation, English from Mando_a")
        self.rows = cursor.fetchall()
        self.unread_dict.clear()

        for row in self.rows:
            self.unread_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.unread_dict.keys()]

class ReadWords(Screen):
    pass

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
    #TODO Add table with scrolling text results - FINISHED
    #TODO See if RV can be combined with scale button - FINISHED
    #TODO Add Message Pop-up to RV Buttons - FINISHED
    #TODO Add Mandoa word to button, add word, pronunciation, and English to pop-up - FINISHED
    #TODO Make immediate refresh after calling reset_databases - FINISHED
    #TODO Figure out why the scrolling db in recycleview starts lower than area -FINISHED- and can be pushed further
    #TODO Page 2 - FINISHED
    #TODO Page 3
    #TODO Page 4
    #TODO Add ability to favorite
    #TODO Edit database to have only unique entries
    #TODO Add what happens when there are no words left
    #TODO Notifications - Plyer
    #TODO Limit length of entries?
    #TODO Make pretty
    #TODO Add touch events
    #TODO Add Search
    #TODO Find if there is a way to stop other py files from loading automatically - maybe putting them in utils?
    #TODO Make it easier to scroll through list (a-z selection?)
    #TODO Set pages to automatically refresh
