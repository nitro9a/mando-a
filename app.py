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
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty

obj_text_list = []

def reset_dbs(self):

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

    create_database('mando-a_read.csv', 'mando-a_read.db', '''CREATE TABLE IF NOT EXISTS Mando_a
    (Mandoa, Pronunciation, English, Read)''', "INSERT INTO Mando_a VALUES (?,?,?,0)")

def add_to_faves(self):

        con = sqlite3.connect('mando-a_favorites.db')
        cursor = con.cursor()
        try:
            w = obj_text_list[0]
            print("OTL:", obj_text_list, type(obj_text_list))
            cursor.execute("SELECT Mandoa from Mando_a WHERE Mandoa=?", (w,))
            entry = cursor.fetchone()

            if w in str(entry):
                pass
            else:
                database.add_word('mando-a_favorites.db', obj_text_list[0], obj_text_list[1], obj_text_list[2], Read=1)

            obj_text_list.clear()

        except IndexError:
            pass

class MessageBox(Popup):



    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):
        global obj_text_list
        super(MessageBox, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('unread').unread_dict[obj.text]
        self.obj_text = word_data[0] + '\n' + word_data[1] + '\n' + word_data[2]

        obj_text_list.extend([word_data[0], word_data[1], word_data[2]])
        print("OBJ TEXT LIST", obj_text_list)

    def add_to_favorites(self):
        add_to_faves(self)

    def checkbox_click(self, instance, value):
        if value is True:
            self.add_to_favorites()
        # if value is False remove from favorites
        else:
            pass

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

    def checkbox_click(self, instance, value):
        if value is True:
            self.add_to_favorites()
        # if value is False remove from favorites
        else:
            pass

class MessageBoxFavorites(Popup):

    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):
        super(MessageBoxFavorites, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('favorites').favorites_dict[obj.text]
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

    word_dict = {}

    get = ObjectProperty(None)
    translation = ObjectProperty(None)

    def __init__(self, **kwargs):
        global obj_text_list
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

                text_result = (f'\n\nWord: {str(word)}\nPronunciation: {str(pro)}\nEnglish: {str(eng)}')
                print("OTL:", obj_text_list, type(obj_text_list))
                obj_text_list.extend([word, pro, eng])
                print("OTL:", obj_text_list, type(obj_text_list))
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

    def add_to_favorites(self):
        add_to_faves(self)

    def checkbox_click(self, instance, value):
        if value is True:
            self.add_to_favorites()
        # if value is False remove from favorites
        else:
            pass

    def reset_checkbox(self):
        for child in reversed(self.ids.grid.children):
            if isinstance(child, CheckBox):
                child.active = False

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

    def reset_databases(self):
        reset_dbs(self)

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

    def reset_databases(self):
        reset_dbs(self)

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

kv = Builder.load_file("layout.kv")

class WordApp(App):
    def build(self):
        return kv

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
    # Figure out why the scrolling db in recycleview starts lower than area -FINISHED
    # Add ability to clear favorites - FINISHED

    #TODO Figure out why the scrolling db in recycleview can be pushed further down and fix it
    #TODO Page 3
    #TODO Page 4
    #TODO Edit database to have only unique entries
    #TODO Add what happens when there are no words left
    #TODO Notifications - Plyer
    #TODO Make pretty
    #TODO Add touch events
    #TODO Add Search
    #TODO Find if there is a way to stop other py files from loading automatically - maybe putting them in utils?
    #TODO Make it easier to scroll through list (a-z selection?) goto_node(key, last_node, last_node_idx)
    #https://kivy.org/doc/stable/api-kivy.uix.recycleview.layout.html
    #TODO Add ability to favorite from page 1 and page 2
    #TODO Add ability to remove favorite individually
    #TODO Add real database and csv files and change code to utilize them in mando_a.py and app.py
    #TODO Add checks: "Are you sure you want to..."
    #TODO Set all labels, buttons, and popups to scale (possibly use scatter, once on touch events are added)
    #TODO Fix clicking on clickbox more than two times causes IndexError: list index out of range
    #TODO Add behavior for unchecking a favorite check box
    #TODO Show "add to favorites" on WordADay page only after word is selected
    #TODO Clear checkboxes so they always are empty after changing word or pages

