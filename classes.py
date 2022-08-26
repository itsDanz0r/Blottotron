import sqlite3

class Blottotron:
    def __init__(self):
        self.bar = []


class Cocktail:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.ingredient_ratio = []

    def make(self, size):
        pass


class Ingredient:
    def __init__(self, name):
        self.name = name
        self.type = ''
        self.pump = None


class Pump:
    def __init__(self):
        self.speed = 255

    def run_pump(self, time):
        pass
