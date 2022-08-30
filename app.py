from hardware_classes import *
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

Window.fullscreen = False
Window.size = (800, 480)

blottotron = Blottotron()
ingredients_list = [Ingredient(name='Vodka'), Ingredient(name='Orange Juice')]


class MasterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heading = Label(
            text='BLOTTOTRON',
            font_size='40',
            font_name='ETHNOCENTRIC (TURBO COVERS)',
            size_hint_y=0.2
        )
        self.bar_label = Label(
            text="Your Bar:\n\nNONE",
            font_size="20",
            halign='center',
            size_hint_y=0.3
        )
        self.add_widget(self.heading)
        self.add_widget(self.bar_label)
        self.orientation = 'vertical'
        self.screen_manager = ScreenManager()
        self.add_screens()
        self.add_widget(self.screen_manager)

    def add_screens(self):
        self.screen_manager.add_widget(MainMenu(parent=self.screen_manager))
        self.screen_manager.add_widget(SettingsMenu(parent=self.screen_manager))
        self.screen_manager.add_widget(IngredientsMenu(parent=self.screen_manager))
        self.screen_manager.current = 'main'

    def update_bar_label(self):
        bar_string = 'Your Bar:\n\n'
        if not blottotron.bar:
            bar_string += 'Empty'
        for ingredient in blottotron.bar:
            bar_string += ingredient.name + ' '
        bar_string.strip()
        self.bar_label.text = bar_string


class BlottotronScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
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
        self.size_hint = (None, None)
        self.size = (210, 210)


class MainMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'main'
        self.size_hint_y = 0.5
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
        super().__init__()
        self.name = 'settings'
        self.ingredients_button = MenuButton(
            text='SELECT\nINGREDIENTS',
            on_release=self.ingredients_menu_clicked
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

    def ingredients_menu_clicked(self, _=None):
        self.parent.current = 'ingredients'


class IngredientsMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'ingredients'
        self.ingredient_buttons = []
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        self.layout.padding = '30dp'
        self.layout.spacing = '20dp'
        self.layout.size_hint_y = None
        self.layout.height = self.layout.minimum_height
        for i in range(0, 10):
            try:
                self.ingredient_buttons.append(Button(
                    text='Ingredient ' + str(i + 1) + ': ' + blottotron.bar[i].name,
                    size_hint=(None, None),
                    size=(400, 50),
                    font_size=20
                )
                )
            except IndexError:
                self.ingredient_buttons.append(Button(
                    text='Ingredient ' + str(i) + ': None',
                    font_size=20,
                    size_hint=(None, None),
                    size=(400, 50),
                )
                )
        self.scroll_view = ScrollView(size_hint=(1, None), size=self.layout.size)
        self.scroll_view.do_scroll_x = False
        self.scroll_view.do_scroll_y = True
        self.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.layout)
        for button in self.ingredient_buttons:
            self.layout.add_widget(button)


class BlottotronApp(App):
    def build(self):
        return MasterLayout()


def main():
    BlottotronApp().run()


if __name__ == '__main__':
    main()
