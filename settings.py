from turtle import width
import pygame as pg

pg.mixer.init()

WIDTH, HEIGHT = 900, 600
WIDTH_GAME = 400
START_POS = 0

# Colors
# Primary Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SAND = (255, 255, 100)
GRAY = (105, 105, 105)

FPS = 240

GRAVITY = 0.7
GRAVITY_TUBE = -0

SAND_HEIGHT = 50

JUMP_VELOCITY = -7
TUBE_VELOCITY = -4
TUBE_WIDTH = 100
SKY_WIDTH = 5
TUBE_GAP = 150

LAYER_DIMS = [5, 1]

POPULATION = 50
NUM_GENNERATION = 500

THRESHOLD = 0.5

FITNESS_RATE = 1

MUTATION_RATE = 0.001
CROSSOVER_RATE = 0.05
# SELECTION_RATE = 0.15  # 0.15

ELITE_PRECENTAGE = 0.2
CROSSOVER_PERCENTAGE = 0.1
# RANDOM_RATE = 0.20

Background  = pg.transform.scale(pg.image.load("images/background.png"), (400, 600))

bird_img = pg.image.load("images/bird.png")
BIRD_SIZE = bird_img.get_size()

