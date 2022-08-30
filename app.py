from hardware_classes import *
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

Window.fullscreen = False
Window.size = (800, 480)

blottotron = Blottotron()
blottotron.bar = [
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None
]

# FOR TESTING PURPOSES ONLY
ingredients_list = [
    None,
    Ingredient(name='Vodka'),
    Ingredient(name='Orange Juice'),
    Ingredient(name='Gin'),
    Ingredient(name='Whisky'),
    Ingredient(name='Coke'),
    Ingredient(name='Triple Sec'),
    Ingredient(name='Raspberry Cordial'),
    Ingredient(name='Absinthe'),
]


class MasterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heading = Label(
            text='BLOTTOTRON',
            font_size='40',
            font_name='Ethnocentric Rg',
            size_hint_y=0.2
        )
        self.bar_label = Label(
            text="Your Bar:\n\nSetup Required",
            font_size="20",
            halign='center',
            size_hint_y=0.3
        )
        self.cocktail_number_label = Label(
            text="\nNo drinks available",
            font_size="20",
            halign='center',
            size_hint_y=0.3
        )
        self.add_widget(self.heading)
        self.add_widget(self.bar_label)
        self.add_widget(self.cocktail_number_label)
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
            if ingredient is None:
                continue
            bar_string += ingredient.name + ' '
        bar_string.strip()
        self.bar_label.text = bar_string


class BlottotronScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.layout = BoxLayout()
        self.layout.orientation = 'horizontal'
        self.layout.padding = '40dp'
        self.layout.spacing = '70dp'

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
        self.size = (260, 210)


class MainMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'main'
        self.size_hint_y = 0.5

        self.pour_button = MenuButton(
            text='\n\nDRINK',
            pos_hint={'x': 0.5}
        )

        self.settings_button = MenuButton(
            text='\n\nSETUP',
            pos_hint={'x': 0.6},
            on_press=self.settings_clicked
        )

        self.widgets = [
            self.pour_button,
            self.settings_button
        ]
        self.add_widgets_to_layout()

    def settings_clicked(self, _=None):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'settings'


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
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'

    def ingredients_menu_clicked(self, _=None):
        self.parent.current = 'ingredients'


class IngredientsMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'ingredients'
        self.ingredient_buttons = []
        self.ingredients_list = []
        self.scroll_view = ScrollView()
        self.setup_layout()
        self.populate_ingredients_list()
        self.setup_buttons()
        self.setup_scrolling()

    def setup_layout(self):
        self.layout = BoxLayout()
        self.layout.orientation = 'vertical'
        self.layout.padding = '30dp'
        self.layout.spacing = '20dp'
        self.layout.size_hint_y = None
        self.layout.height = 660

    def populate_ingredients_list(self):
        for ingredient in ingredients_list:
            if ingredient is None:
                self.ingredients_list.append(
                    'None'
                )
            else:
                self.ingredients_list.append(
                    ingredient.name
                )

    def setup_scrolling(self):
        self.scroll_view.do_scroll_x = False
        self.add_widget(self.scroll_view)

        self.scroll_view.add_widget(self.layout)

    def setup_buttons(self):
        for i in range(0, 10):
            try:
                self.ingredient_buttons.append(Spinner(
                    text='Ingredient ' + str(i + 1) + ': ' + blottotron.bar[i].name,
                    size_hint_y=None,
                    height=50,
                    size_hint_x=0.6,
                    pos_hint={'x': 0.2},
                    font_size=20,
                    values=self.ingredients_list,
                )
                )

            except AttributeError:
                self.ingredient_buttons.append(Spinner(
                    text='Ingredient ' + str(i + 1) + ': None',
                    size_hint_y=None,
                    height="40dp",
                    values=self.ingredients_list,
                    size_hint_x=0.6,
                    pos_hint={'x': 0.2},
                )
                )

        for button in self.ingredient_buttons:
            self.layout.add_widget(button)

        self.layout.add_widget(
            Button(
                text="Save",
                size_hint_x=0.6,
                size_hint_y=None,
                pos_hint={'x': 0.2},
                height="70dp",
                on_release=self.save_and_return,
            )
        )

    def save_and_return(self, _=None):
        for index, spinner in enumerate(self.ingredient_buttons):
            if spinner.text in self.ingredients_list:
                blottotron.bar[index] = Ingredient(name=spinner.text)
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'
        self.parent.parent.update_bar_label()


class BlottotronApp(App):
    def build(self):
        master_layout = MasterLayout()
        return master_layout


def main():
    BlottotronApp().run()


if __name__ == '__main__':
    main()
