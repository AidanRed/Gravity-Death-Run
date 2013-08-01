from pyglet.window import key
from pyglet.sprite import Sprite


class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Player(object):
    def __init__(self, x, y, image, batch, windowSize):
        self.windowSize = windowSize

        self.sprite = Sprite(image, x=x, y=y, batch=batch)

        self.halfHeight = image.height / 2
        self.halfWidth = image.width / 2

        self.dx = 0
        self.dy = 0

        self.gravity = -500

        self.allowPress = True

        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        ##Changed to make the movement less 'elastic' and instead more responsive
        #self.dy += self.gravity * dt

        #self.sprite.y += self.dy * dt
        self.sprite.y += self.gravity * dt
        self.sprite.x += self.dx * dt

        self.dy = self.gravity

        if self.sprite.y - self.halfHeight < 0:
            self.sprite.y = 0 + self.halfHeight
            self.dy = 0

        elif self.sprite.y + self.halfHeight > self.windowSize.height:
            self.sprite.y = self.windowSize.height - self.halfHeight
            self.dy = 0

        if self.key_handler[key.SPACE] and self.allowPress:
            self.gravity = -self.gravity
            self.allowPress = False

        elif not self.key_handler[key.SPACE] and not self.allowPress:
            self.allowPress = True
