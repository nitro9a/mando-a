from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

long_text = 'yay moo cow foo bar moo baa ' * 100

Builder.load_string('''
<ScrollableLabel@Label>:
    
    bcolor: 1,1,1,1
    canvas.before:
        PushMatrix
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        PopMatrix
       
        
  
        
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class ScrollApp(App):
    def build(self):
        return ScrollableLabel(text=long_text)

if __name__ == "__main__":
    ScrollApp().run()