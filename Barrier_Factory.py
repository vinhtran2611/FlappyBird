from turtle import width
from Sky import *
from Bird import *
from Ground import *
from settings import *
from Tube import *
import random


# Design Pattern : Factory
class Barrier_Factory:
    def __init__(self):
        self.index = 0
        self.tube_heights = []

        for i in range(1, 3000):
            self.tube_heights.append(random.randint(10, HEIGHT - SAND_HEIGHT - TUBE_GAP - 10))

        self.count = 0

        tube = Tube(0, 0, 0, 0)
        sky = Sky(0, 0, 0, 0)
        ground = Ground(0, 0, 0, 0)

        self.dict = {"Tube": type(tube), "Sky": type(sky), "Ground": type(ground)}

    def generate(self, barrier_name):
        self.count += 1

        if barrier_name == "Sky":
            sky = Sky(START_POS, 0, WIDTH_GAME, SKY_WIDTH)
            if type(sky) is self.dict["Sky"]:
                return sky

        if barrier_name == "Ground":
            ground = Ground(START_POS, HEIGHT - SAND_HEIGHT, WIDTH_GAME, SAND_HEIGHT)
            if type(ground) is self.dict["Ground"]:
                return ground

        if barrier_name == "Tube":
            self.index += 1
            TUBE_HEIGHT = random.randint(20, HEIGHT - SAND_HEIGHT - TUBE_GAP - 20)

            tube_top = Tube(WIDTH_GAME, SKY_WIDTH, TUBE_WIDTH, TUBE_HEIGHT)
            tube_bottom = Tube(WIDTH_GAME, TUBE_HEIGHT + TUBE_GAP, TUBE_WIDTH, HEIGHT - SAND_HEIGHT - (TUBE_HEIGHT + TUBE_GAP))

            if type(tube_top) and type(tube_bottom) is self.dict["Tube"]:
                return tube_top, tube_bottom

        raise NameError("Wrong factory format")
