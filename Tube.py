from settings import *

vec2 = pg.math.Vector2


class Tube(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = h

        # This is the tubes x velocity, giving the appearance of the player moving
        self.velX = TUBE_VELOCITY

    def update(self):
        # This is the cause of the tubes movement
        self.velX += GRAVITY_TUBE
        # print(f'Before: {self.rect.x}, After: {self.rect.x + self.velX}')
        self.rect.x += self.velX

        # If a tube goes of the screen then it is 'killed'
        if self.rect.x <= -TUBE_WIDTH:
            self.kill()
        
