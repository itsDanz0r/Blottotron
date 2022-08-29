import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from kivy.uix.image import Image

Window.fullscreen = False
Window.size = (800, 480)

kivy.require('2.1.0')


class MasterLayout(BoxLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text='BLOTTOTRON',
            font_size='40',
            font_name='ETHNOCENTRIC (TURBO COVERS)',
            size_hint_y=0.3,
            pos_hint={'y': 1}
        )
        self.add_widget(self.label)
        self.orientation = 'vertical'


class BlottotronScreen(Screen):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.layout = BoxLayout()
        self.layout.orientation = 'horizontal'
        self.layout.padding = '50dp'
        self.layout.spacing = '30dp'

        self.widgets = []
        self.add_widget(self.layout)

    def add_widgets_to_layout(self):
        for widget in self.widgets:
            self.layout.add_widget(widget)


class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = 'center'
        self.font_size = 25
        self.size_hint_y = 0.7


class MainMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__(parent=None)
        self.name = 'main'
        self.size_hint_y = 1
        self.pour_button = MenuButton(
            text='\n\nDRINK',
        )
        self.status_button = MenuButton(
            text='\n\nSTATUS',
        )

        self.settings_button = MenuButton(
            text='\n\nSETUP',
            on_press=self.settings_clicked
        )

        self.widgets = [
            self.pour_button,
            self.status_button,
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
        self.ingredients_button = MenuButton(
            text='SELECT\nINGREDIENTS',
        )
        self.back_button = MenuButton(
            text='RETURN TO\nMENU',
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
        master_layout = MasterLayout(None)
        screen = ScreenManager()
        screen.add_widget(MainMenu(parent=screen))
        screen.add_widget(SettingsMenu(parent=screen))

        screen.current = 'main'
        master_layout.add_widget(screen)
        return master_layout


if __name__ == '__main__':
    BlottotronApp().run()
