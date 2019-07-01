import sqlite3
import random
from utils import database
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label



white = (1,1,1,1)
black = (0,0,0,0)
yellow = (.9, .8, 0, 1)
red = (.9, .3, 0, 1)
orange = (.9, .5, 0, 1)

class appLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(appLayout, self).__init__(**kwargs)
        self.button= Button(text= 'Click Here', font_size = 30, color = yellow, pos_hint = {'center_x': 0.5, 'center_y': .8}, size_hint = (.25, .25))
        self.label = Label(text = 'Hello')
        self.button.bind(on_press = self.update_3)

        self.add_widget(self.button)
        self.add_widget(self.label)

    def update(self, event):
        self.label.text = self.random_number()

    def update_2(self, event):
        my_dict = {
            'One': random.randrange(0,100),
            'Two': random.randrange(0,100),
            'Three': random.randrange(0,100)
        }

        my_dict_formatted = (f'One: {my_dict["One"]} \nTwo: {my_dict["Two"]}\nThree:{my_dict["Three"]}\n')

        self.label.text = str(my_dict_formatted)

    def update_3(self, event):
        my_dict = {
            'One': random.randrange(0,100),
            'Two': random.randrange(0,100),
            'Three': random.randrange(0,100)
        }

        word = my_dict["One"]
        pronunciation = my_dict["Two"]
        english = my_dict["Three"]

        print (word, pronunciation, english)

        self.label.text = (f'Word: {str(word)}\nPronunciation: {str(pronunciation)}\nEnglish: {str(english)}')


    def random_number(self):
        num = str(random.randrange(0,100))
        return num


class WordApp(App):

    def build(self):
        appL = appLayout()
        return appL

if __name__=="__main__":
    WordApp().run()