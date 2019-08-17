import sqlite3
import csv
import random
import plyer
from plyer import notification, facades
from utils import database, scalelabel, scrollablelabel
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.effects import kinetic, scroll
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview.views import _cached_views, _view_base_cache

dgrey = (45/255, 45/255, 45/255, 1)
red = (155/255, 10/255, 10/255, 1)
white = (1,1,1,1)

obj_text_list = []

current_word = "test"

def reset_dbs(self):

    def create_database(csv_file, database, execute_create, execute_insert):
        f = open(csv_file,'r', encoding='utf-8', errors= 'ignore')  # TEMPORARY FIX
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

    create_database('mando-a.csv', 'mando-a_all.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

    create_database('mando-a.csv', 'mando-a_unread.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

    create_database('mando-a_read.csv', 'mando-a_read.db', '''CREATE TABLE IF NOT EXISTS Mando_a
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

def add_to_faves(self):
    con = sqlite3.connect('mando-a_favorites.db')
    cursor = con.cursor()
    global current_word
    try:
        w = obj_text_list[0]
        current_word = obj_text_list[0]
        cursor.execute("SELECT Mandoa from Mando_a WHERE Mandoa=?", (w,))
        entry = cursor.fetchone()

        if w in str(entry):
            pass
        else:
            database.add_word('mando-a_favorites.db', obj_text_list[0], obj_text_list[1], obj_text_list[2], Read=1)

    except IndexError:
        pass

    obj_text_list.clear()

class MessageBox(Popup):
    global obj_text_list
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):

        super(MessageBox, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('unread').unread_dict[obj.text]
        self.obj_text = word_data[0] + '\n' + word_data[1] + '\n' + word_data[2]

        obj_text_list.extend([word_data[0], word_data[1], word_data[2]])

    def add_to_favorites(self):
        add_to_faves(self)

    def clear(self):
        obj_text_list.clear()

class MessageBoxRead(Popup):

    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):
        global obj_text_list
        super(MessageBoxRead, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('read').read_dict[obj.text]
        self.obj_text = word_data[0] + '\n' + word_data[1] + '\n' + word_data[2]

        obj_text_list.extend([word_data[0], word_data[1], word_data[2]])

    def add_to_favorites(self):
        add_to_faves(self)

    def clear(self):
        obj_text_list.clear()

class MessageBoxFavorites(Popup):
    favorite_list = []
    current_favorite = ''
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):

        super(MessageBoxFavorites, self).__init__(**kwargs)
        self.obj = obj

        word_data = kv.get_screen('favorites').favorites_dict[obj.text]
        self.obj_text = word_data[0] + '\n' + word_data[1] + '\n' + word_data[2]
        self.favorite_list.extend([word_data[0], word_data[1], word_data[2]])

    def remove_from_favorites(self):

        con = sqlite3.connect('mando-a_favorites.db')
        cursor = con.cursor()

        try:
            w = self.favorite_list[0]
            self.current_favorite = self.favorite_list[0]
            cursor.execute("SELECT Mandoa from Mando_a WHERE Mandoa=?", (w,))
            entry = cursor.fetchone()
            database.remove_word('mando-a_favorites.db', w)

        except IndexError:
            pass

    def clear(self):
        self.favorite_list.clear()

class MessageBoxFinished(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_databases(self):
        reset_dbs(self)

class MessageBoxConfirmation(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_databases(self):
        reset_dbs(self)

class MessageBoxFavoritesConfirmation(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_favorites(self):
        Favorites.reset_favorites(self)

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
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def update_changes(self, txt):
        self.text = txt

class SelectableButtonUnread(SelectableButton):
    def on_press(self):
        popup = MessageBox(self)
        popup.open()

class SelectableButtonRead(SelectableButton):
    def on_press(self):
        popup = MessageBoxRead(self)
        popup.open()

class SelectableButtonFavorites(SelectableButton):
    def on_press(self):
        popup = MessageBoxFavorites(self)
        popup.open()

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class WindowManager(ScreenManager):
    pass

class WordADay(Screen):
    word_a_day = []
    word_dict = {}

    get = ObjectProperty(None)
    translation = ObjectProperty(None)

    def __init__(self, **kwargs):
        #global obj_text_list
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
            self.word_a_day.clear()
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

                text_result = (f'Word: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')
                self.word_a_day.extend([word, pro, eng])

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
            popup = MessageBoxFinished()
            popup.open()

        elif rowcount >= 1:
            get_random_word()

    def add_to_favorites(self):
        con = sqlite3.connect('mando-a_favorites.db')
        cursor = con.cursor()

        try:
            w = self.word_a_day[0]
            cursor.execute("SELECT Mandoa from Mando_a WHERE Mandoa=?", (w,))
            entry = cursor.fetchone()

            if w in str(entry):
                pass
            else:
                database.add_word('mando-a_favorites.db', self.word_a_day[0], self.word_a_day[1], self.word_a_day[2], Read=1)

        except IndexError:
            print(IndexError)

    obj_text_list.clear()

    def checkbox_click(self, instance, value):
        if value is True:
            self.add_to_favorites()

class UnreadWords(Screen):

    unread_dict = {}

    unread_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Mandoa", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(UnreadWords, self).__init__(**kwargs)
        self.unread_dict = {}

    def display_database(self):
        con = sqlite3.connect('mando-a_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT Mandoa, Pronunciation, English from Mando_a")
        self.rows = cursor.fetchall()
        self.unread_dict.clear()
        ReadWords.read_dict.clear()
        Favorites.favorites_dict.clear()

        for row in self.rows:
            self.unread_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.unread_dict.keys()]

    def confirmation_popup(self):
        popup = MessageBoxConfirmation()
        popup.open()

class ReadWords(Screen):

    read_dict = {}

    read_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Mandoa", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(ReadWords, self).__init__(**kwargs)
        self.read_dict = {}

    def display_database(self):
        con = sqlite3.connect('mando-a_read.db')
        cursor = con.cursor()
        cursor.execute("SELECT Mandoa, Pronunciation, English from Mando_a")
        self.rows = cursor.fetchall()
        self.read_dict.clear()
        UnreadWords.unread_dict.clear()
        Favorites.favorites_dict.clear()

        for row in self.rows:
            self.read_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.read_dict.keys()]

    def confirmation_popup(self):
        popup = MessageBoxConfirmation()
        popup.open()

class Favorites(Screen):

    favorites_dict = {}

    favorites_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Mandoa", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(Favorites, self).__init__(**kwargs)
        self.favorites_dict = {}

    def display_database(self):
        con = sqlite3.connect('mando-a_favorites.db')
        cursor = con.cursor()
        cursor.execute("SELECT Mandoa, Pronunciation, English from Mando_a")
        self.rows = cursor.fetchall()
        self.favorites_dict.clear()
        UnreadWords.unread_dict.clear()
        ReadWords.read_dict.clear()

        for row in self.rows:
            self.favorites_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.favorites_dict.keys()]

    def reset_favorites(database):

        def delete_favorites(database):
            sql = sqlite3.connect(database)
            cursor = sql.cursor()
            cursor.execute("DROP TABLE Mando_a")

        def create_favorites(csv_file, database, execute_create, execute_insert):
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

        delete_favorites("mando-a_favorites.db")

        create_favorites('mando-a_favorites.csv', 'mando-a_favorites.db', '''CREATE TABLE IF NOT EXISTS Mando_a 
        (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

    def confirmation_popup(self):
        popup = MessageBoxFavoritesConfirmation()
        popup.open()

class Test(Screen):
    pass

kv = Builder.load_file("layout.kv")

class WordApp(App):
    def build(self):
        return kv
    def on_start(self):

        self.root.get_screen('unread').display_database()
        self.root.get_screen('read').display_database()
        self.root.get_screen('favorites').display_database()

        #to set current page at start use: self.root.current = ('word')

if __name__=="__main__":
    WordApp().run()

    # look at exercise dice, gen_ex_die, for line in text - figure out text wrapping - FINISHED
    # Make pages - FINISHED
    # Create a new list of unread words, 'remove word' from 'unread word' list - FINISHED
    # Add random word to a 'read words' list - FINISHED
    # Figure out why program is crashing seemingly randomly on random choice - FINISHED
    # Add reset - FINISHED

    # Figure out how to make page navigation buttons uniform even when the rest of the layout is different (it works,
    # continued... if you use the same amount of layouts no matter their size.  Can probably adjust padding for
    # different number of layouts - FINISHED
    # Add table with scrolling text results - FINISHED
    # See if RV can be combined with scale button - FINISHED
    # Add Message Pop-up to RV Buttons - FINISHED
    # Add Mandoa word to button, add word, pronunciation, and English to pop-up - FINISHED
    # Make immediate refresh after calling reset_databases - FINISHED

    # Page 2 - FINISHED
    # Add ability to favorite - FINISHED
    # Check if favorite exists before adding it to db - FINISHED
    # Set colors as variables - FINISHED
    # Set pages to automatically refresh - FINISHED
    # Figure out why the scrolling db in recycleview starts lower than area - FINISHED

    # Add ability to clear favorites - FINISHED
    # Clear checkboxes so they always are empty after changing word or pages - FINISHED
    # Add ability to favorite from page 1 and page 2 - FINISHED
    # Clear CheckBox on "Get a Word" - FINISHED
    # Page 3 - FINISHED
    # Add ability to remove favorite individually - FINISHED

    # Show "add to favorites" on WordADay page only after word is selected - FINISHED
    # Fix clicking on clickbox (now button) more than two times causes IndexError: list index out of range - FINISHED
    # Finished and reset dictionaries (FINISHED) need to clear WordADay add to favorites checkbox (now button), will
    # not add to favorites after clear - possible fix this by removing globals like in Favorites/remove from favorites - FINISHED
    # Page 4 - FINISHED
    # Add what happens when there are no words left - FINISHED
    # Add checks: "Are you sure you want to..." - FINISHED

    # Add real database and csv files and change code to utilize them in mando_a.py and main.py - FINISHED
    # Fix issue with page visibly refreshing upon selecting page - FINISHED
    # Add touch events - FINISHED (unnecessary)
    # fix issue with page visibly refreshing upon selecting page - FINISHED
    # Edit database to have only unique entries; edit for consistency - FINISHED
    # disable favorites button when it isn't in use - FINISHED
    # Set all labels, buttons, and popups to scale (possibly use scatter, once on touch events are added)- FINISHED

    # remove page titles since they are already on tabs - FINISHED
    # normalize page layouts - FINISHED

    #TODO Figure out why the scrolling db in recycleview can be pushed further down and fix it
    #TODO Make pretty
    #TODO Change colors of intividual parts of translation
    #TODO Notifications - Plyer
    #TODO remove test csv and databases
    #TODO change icons, favicons
    #TODO add images for backgound normal/down

    #TODO Add Search
    #TODO Dynamically Refine Search
    #TODO Make it easier to scroll through list (a-z selection?) goto_node(key, last_node, last_node_idx)
    #https://kivy.org/doc/stable/api-kivy.uix.recycleview.layout.html
    #see scroll effect
    #TODO Word a Day Android Widget
    #TODO add random Mando phrases to the loading page
    #TODO add color options






    