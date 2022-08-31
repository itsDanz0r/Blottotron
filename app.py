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
            text='\n\nBLOTTOTRON',
            font_size='50',
            font_name='Ethnocentric (Turbo Covers)',
            size_hint_y=0.2,
            pos_hint={'y':0.3}
        )

        self.add_widget(self.heading)
        self.orientation = 'vertical'
        self.screen_manager = ScreenManager()
        self.add_screens()
        self.add_widget(self.screen_manager)

    def add_screens(self):
        self.screen_manager.add_widget(MainMenu(parent=self.screen_manager))
        self.screen_manager.add_widget(SettingsMenu(parent=self.screen_manager))
        self.screen_manager.add_widget(IngredientsMenu(parent=self.screen_manager))
        self.screen_manager.current = 'main'


class BlottotronScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.layout = BoxLayout()
        self.layout.orientation = 'horizontal'
        self.layout.padding = [75, 0, 75, 40]
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
        self.size = (300, 210)
        self.font_name = 'Minimalust Regular'


class MainMenu(BlottotronScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'main'
        self.size_hint_y = 0.5

        self.pour_button = MenuButton(
            text='\n\n\n\ndrink',
        )

        self.settings_button = MenuButton(
            text='\n\n\n\nsetup',
            on_press=self.settings_clicked
        )

        self.pour_icon = Image(
            source='./img/cocktail_icon.png',
        )

        self.settings_icon = Image(
            source='./img/settings_icon.png',
        )

        self.widgets = [
            self.pour_button,
            self.settings_button,
        ]
        self.add_widgets_to_layout()
        self.place_button_icons()

    def place_button_icons(self):
        self.pour_button.add_widget(self.pour_icon)
        self.pour_icon.x = self.pour_button.x + 178
        self.pour_icon.y = self.pour_button.y + 125

        self.settings_button.add_widget(self.settings_icon)
        self.settings_icon.x = self.settings_button.x + 542
        self.settings_icon.y = self.settings_button.y + 125


    def settings_clicked(self, _=None):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'settings'


class SettingsMenu(BlottotronScreen):

    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'settings'
        self.ingredients_button = MenuButton(
            text='\n\n\n\ningredients',
            on_release=self.ingredients_menu_clicked
        )
        self.back_button = MenuButton(
            text='\n\n\n\nmenu',
            on_release=self.main_menu_clicked
        )
        self.back_icon = Image(
            source='./img/back_icon.png'
        )
        self.ingredients_icon = Image(
            source='./img/ingredients_icon.png'
        )
        self.widgets = [
            self.ingredients_button,
            self.back_button
        ]
        self.add_widgets_to_layout()
        self.place_button_icons()

    def main_menu_clicked(self, _=None):
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'

    def ingredients_menu_clicked(self, _=None):
        self.parent.current = 'ingredients'

    def place_button_icons(self):
        self.ingredients_button.add_widget(self.ingredients_icon)
        self.ingredients_icon.x = self.ingredients_button.x + 178
        self.ingredients_icon.y = self.ingredients_button.y + 125

        self.back_button.add_widget(self.back_icon)
        self.back_icon.x = self.back_button.x + 542
        self.back_icon.y = self.back_button.y + 125


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
        self.layout.height = 720

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


class BlottotronApp(App):
    def build(self):
        master_layout = MasterLayout()
        return master_layout


def main():
    BlottotronApp().run()


if __name__ == '__main__':
    main()
