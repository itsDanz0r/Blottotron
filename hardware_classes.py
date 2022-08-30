import sqlite3
import RPi.GPIO as GPIO
import time


class Blottotron:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.bar = []

    def setup_bar(self, ingredients_list):
        self.bar = ingredients_list


class Cocktail:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.ingredient_ratio = []

    def make(self, size):
        for i in range(len(self.ingredients)):
            pour_volume = size
            self.ingredients[i].pour(pour_volume)


class Ingredient:
    def __init__(self, name):
        self.name = name
        self.type = ''
        self.pump = None
        self.volume_remaining = 0

    def pour(self, volume):
        run_time = volume * 150
        # Pour volume is ~150ml/s @ 490hz 25% DC
        self.pump.run_pump(run_time)


class Pump:
    def __init__(self, pwm_pin):
        self.speed = 255
        GPIO.setup(pwm_pin, GPIO.OUT)
        self.pwm_pin = pwm_pin
        self.pwm = GPIO.PWM(self.pwm_pin, 490)

    def run_pump(self, run_time):
        start_time = time.time()
        end_time = start_time + run_time
        while time.time() < end_time:
            self.pwm.start(25)
        self.pwm.stop()
