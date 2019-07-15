from kivy.app import App
from kivy.lang import Builder
from utils import scalelabel
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, StringProperty

root = Builder.load_string('''
<RV>:
    viewclass: 'SelectableButton'
    RecycleBoxLayout:
        bcolor: 1,1,1,1         
        padding: "15dp", "5dp", "15dp", "15dp"
        default_size: None, dp(25)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        
<SelectableButton>:
    state_image: self.background_normal if self.state == 'normal' else self.background_down
	disabled_image: self.background_disabled_normal if self.state == 'normal' else self.background_disabled_down
	_scale: 1. if self.texture_size[0] < self.width else float(self.width) / self.texture_size[0]
	orientation: 'horizontal'
    # Draw a background to indicate selection
    canvas:
        Color:
            rgba: self.background_color
        BorderImage:
            border: self.border
            pos: self.pos
            size: self.size
            source: self.disabled_image if self.disabled else self.state_image
        PushMatrix
        Scale:
            origin: self.center
            x: self._scale or 1.
            y: self._scale or 1.
        Color:
            rgba: self.disabled_color if self.disabled else self.color
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
        PopMatrix

        
''')

class MessageBox(Popup):
    def popup_dismiss(self):
        self.dismiss()

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """

class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)
    def on_press(self):
        pass
    def on_release(self):
        MessageBox().open()

class RV(RecycleView):
    rv_layout = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class RecycleApp(App):
    def build(self):
        return root
