import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window

Window.fullscreen = False

kivy.require('2.1.0')


class BlottotronScreen(Screen):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.parent = parent
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        self.layout.padding = '30dp'
        self.layout.spacing = '30dp'
        self.layout.size_hint_x = 0.7
        self.layout.pos_hint = {'x': 0.15}
        self.widgets = []
        self.add_widget(self.layout)

    def add_widgets_to_layout(self):
        for widget in self.widgets:
            self.layout.add_widget(widget)


class MainMenu(BlottotronScreen):

    def __init__(self, **kwargs):
        super().__init__(parent=None)
        self.name = 'main'
        self.pour_button = Button(
            text='POUR\nCOCKTAIL',
            halign='center',
            font_size=30
        )
        self.settings_button = Button(
            text='SETTINGS',
            halign='center',
            font_size=30,
            size_hint_y=0.7,
            on_press=self.settings_clicked
        )
        self.widgets = [
            self.pour_button,
            self.settings_button
        ]
        self.add_widgets_to_layout()

    def settings_clicked(self, _=None):
        self.parent.current = 'settings'
        self.parent.transition = SlideTransition(direction='right')


class SettingsMenu(BlottotronScreen):

    def __init__(self, **kwargs):
        super().__init__(parent=None)
        self.name = 'settings'
        self.ingredients_button = Button(
            text='SELECT\nINGREDIENTS',
            halign='center',
            font_size=30
        )
        self.back_button = Button(
            text='RETURN TO\nMENU',
            halign='center',
            font_size=30,
            size_hint_y=0.7,
            on_release=self.main_menu_clicked
        )
        self.widgets = [
            self.ingredients_button,
            self.back_button
        ]
        self.add_widgets_to_layout()

    def main_menu_clicked(self, _=None):
        self.parent.current = 'main'
        self.parent.transition = SlideTransition(direction='left')



class BlottotronApp(App):
    def build(self):
        screen = ScreenManager()
        screen.add_widget(MainMenu(parent=screen))
        screen.add_widget(SettingsMenu(parent=screen))

        screen.current = 'main'
        return screen


if __name__ == '__main__':
    app().run()
