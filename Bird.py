from matplotlib import image
from Sensor import *
from ANN import *
from Sensor import Sensor

vec2 = pg.math.Vector2


class Bird(pg.sprite.Sprite):
    def __init__(self,  layer_dims = LAYER_DIMS, genome=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/blue_bird.png')        
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH_GAME / 2 + 50 , random.randint(15, HEIGHT - SAND_HEIGHT) - 5)

        # self.pos = vec2(WIDTH_GAME/2, HEIGHT/2)
        self.pos = vec2(START_POS + WIDTH_GAME/ 2, random.randint(15, HEIGHT - SAND_HEIGHT) - 5)

        self.vel = vec2(0, 0)
        self.acc = vec2(0, GRAVITY)

        self.live = 1

        self.sensor = Sensor()

        if genome is None:
            self.ANN = ANN(layer_dims = layer_dims)
        else:
            self.ANN = ANN(layer_dims, genome)


    def update(self):
        self.vel += self.acc
        self.pos += self.vel + self.acc
        self.rect.center = (self.pos[0], self.pos[1])

        if self.live == 1:  # if bird alive then increase fitness
            self.ANN.fitness += FITNESS_RATE

    def flap(self):
        self.vel.y = JUMP_VELOCITY
