"""
TODO:
 - Change the players position so that they are closer to the left-hand side of the screen, so that they can better
   see incoming obstacles.
"""
from pyglet.window import key
import pyglet
from vectors import Vector2
from simpleLibrary import SEPARATOR
import math


class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class PlayerBullet(object):
    def __init__(self, x, y, batch, windowSize, player):
        image = pyglet.image.load("resources" + SEPARATOR + "playerBullet.png")
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch)

        self.bulletSpeed = 500
        self.velocity = Vector2(self.bulletSpeed, 0)

        self.player = player

        self.windowSize = windowSize

        self.destroyed = False

    def update(self, dt):
        if not self.destroyed:
            self.velocity.y += (self.player.gravity * 3) * dt

            self.sprite.rotation = math.degrees(self.velocity.getAngle())

            self.sprite.x += self.velocity.x * dt
            self.sprite.y += self.velocity.y * dt

            if self.sprite.x > self.windowSize.width or self.sprite.x < 0:
                self.destroy()

            if self.sprite.y > self.windowSize.height or self.sprite.y < 0:
                self.destroy()

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.sprite.delete()


class Player(object):
    def __init__(self, x, y, image, batch, windowSize):
        self.windowSize = windowSize

        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch)

        self.halfHeight = image.height / 2
        self.halfWidth = image.width / 2

        self.dx = 0
        self.dy = 0

        self.gravity = -500

        self.allowPress = True

        self.allowKeypress = {key.ENTER : True, key.SPACE : True}
        self.key_handler = key.KeyStateHandler()

        self.bullets = []

    def update(self, dt):
        ##Changed to make the movement less 'elastic' and instead more responsive
        #self.dy += self.gravity * dt

        #self.sprite.y += self.dy * dt

        #Remove all the destroyed bullets from the list
        newBulletList = []
        for bullet in self.bullets:
            if not bullet.destroyed:
                bullet.update(dt)
                newBulletList.append(bullet)

            else:
                del bullet

        self.bullets = newBulletList

        self.sprite.y += self.gravity * dt
        self.sprite.x += self.dx * dt

        self.dy = self.gravity

        if self.sprite.y - self.halfHeight < 0:
            self.sprite.y = 0 + self.halfHeight
            self.dy = 0

        elif self.sprite.y + self.halfHeight > self.windowSize.height:
            self.sprite.y = self.windowSize.height - self.halfHeight
            self.dy = 0

        #Set 'enter' to flip gravity
        if self.key_handler[key.ENTER] and self.allowKeypress[key.ENTER]:
            self.gravity = -self.gravity
            self.allowKeypress[key.ENTER] = False

        elif not self.key_handler[key.ENTER] and not self.allowKeypress[key.ENTER]:
            self.allowKeypress[key.ENTER] = True

        #Set 'space' to fire a bullet
        if self.key_handler[key.SPACE] and self.allowKeypress[key.SPACE]:
            self.bullets.append(PlayerBullet(self.sprite.x, self.sprite.y, self.sprite.batch, self.windowSize, self))
            self.allowKeypress[key.SPACE] = False

        elif not self.key_handler[key.SPACE] and not self.allowKeypress[key.SPACE]:
            self.allowKeypress[key.SPACE] = True


class TileMap(object):
    def __init__(self, windowSize):
        #The keys for the dictionary is the column number that you want to access.
        self.data = {}
        self.windowSize = windowSize

        self.leftColumnOffset = 0
        self.rightColumnOffset = 0

        self.bottomLeft = Vector2(0, 0)

        self.scrollSpeed = 500

    def update(self, dt):
        self.bottomLeft.x += self.scrollSpeed
