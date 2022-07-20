from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

from BulkSpanishdict import translateList

Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class BulkSpanishDict(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.9)
        self.window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.textInput = TextInput(multiline = True, padding_y = (10,10))
        self.window.add_widget(self.textInput)

        self.submitButton = Button(text="Translate", size_hint=(1,0.3), background_color='#00FFCE')
        self.submitButton.bind(on_press=self.translate)
        self.window.add_widget(self.submitButton)

        self.textOutput = ScrollableLabel(text = '...')
        self.window.add_widget(self.textOutput)

        return self.window
    
    def translate(self, instance):
        self.textOutput.text = translateList(self.textInput.text)

if __name__ == "__main__":
    BulkSpanishDict().run()