"""
TODO:
 + Change the players position so that they are closer to the left-hand side of the screen, so that they can better
   see incoming obstacles.
"""
from pyglet.window import key
import pyglet
from libs.vectors import Vector2
from libs.simpleLibrary import SEPARATOR
from libs import boundingShapes
import math
import random
import shelve

class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Projectile(object):
    def __init__(self, x, y, image, batch, windowSize, player, speed, gravity, boundingType="rectangle", spin=0):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch)

        self.gravity = gravity

        self.speed = speed
        self.velocity = Vector2(self.speed, 0)

        self.player = player

        self.windowSize = windowSize

        self.destroyed = False

        self.spin = spin

        if boundingType.lower() == "rectangle":
            self.boundingShape = boundingShapes.Rectangle((x, y), image.width, image.height)

        elif boundingType.lower() == "circle":
            radius = max(image.width, image.height)
            self.boundingShape = boundingShapes.Circle((image.x, image.y), radius)

    def update(self, dt):
        if not self.destroyed:
            if self.player.gravity < 0 and self.gravity > 0:
                self.gravity = -self.gravity
            elif self.player.gravity > 0 and self.gravity < 0:
                self.gravity = -self.gravity

            self.velocity.y += self.gravity  * dt

            if self.spin == 0:
                self.sprite.rotation = 360 - math.degrees(self.velocity.getAngle())

            if self.spin != 0:
                self.sprite.rotation += self.spin * dt

            self.sprite.x += self.velocity.x * dt
            self.sprite.y += self.velocity.y * dt

            if self.sprite.x - self.sprite.width > self.windowSize.width or self.sprite.x + self.sprite.width < 0:
                self.destroy()

                #Removed to allow the projectile to go off the sides of the screen
                ##if self.sprite.y > self.windowSize.height or self.sprite.y < 0:
                ##    self.destroy()

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.sprite.delete()


class PlayerBullet(Projectile):
    def __init__(self, x, y, batch, windowSize, player):
        image = pyglet.image.load("resources" + SEPARATOR + "playerBullet.png")

        bulletSpeed = 1500
        gravity = player.gravity * 2

        super(PlayerBullet, self).__init__(x, y, image, batch, windowSize, player, bulletSpeed, gravity)


class PlayerRocket(Projectile):
    def __init__(self, x, y, batch, windowSize, player):
        image = pyglet.image.load("resources" + SEPARATOR + "playerRocket.png")

        rocketSpeed = 400
        gravity = player.gravity * 2

        super(PlayerRocket, self).__init__(x, y, image, batch, windowSize, player, rocketSpeed, gravity)


class PlayerCannonball(Projectile):
    def __init__(self, x, y, batch, windowSize, player):
        image = pyglet.image.load("resources" + SEPARATOR + "playerCannonball.png")

        cannonballSpeed = 500
        gravity = 0

        super(PlayerCannonball, self).__init__(x, y, image, batch, windowSize, player, cannonballSpeed, gravity, spin=300.0)


class Player(object):
    def __init__(self, x, y, image, batch, windowSize):
        self.windowSize = windowSize

        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y, batch=batch)

        self.halfHeight = image.height / 2
        self.halfWidth = image.width / 2

        self.gravity = -1000

        self.velocity = Vector2(0, self.gravity)

        self.acceleration = Vector2(0, 0)

        self.allowPress = True

        self.allowKeypress = {key.ENTER : True, key.SPACE : True, key.RIGHT : True, key.LEFT : True}
        self.key_handler = key.KeyStateHandler()

        self.jetpackPower = 30

        self.bullets = []

        self.equippedWeapon = 0

        self.weaponList = ["pistol", "cannon", "rocket"]

        self.spriteHidingPlace = Vector2(-100, -100)

        flameImage = pyglet.image.load("resources" + SEPARATOR + "flame1.png")

        self.rocketSprite = pyglet.sprite.Sprite(flameImage, x=self.spriteHidingPlace.x,
                                                 y=self.spriteHidingPlace.y, batch=batch)

        self.invertedRocketSprite = pyglet.sprite.Sprite(flameImage, x=self.spriteHidingPlace.x,
                                                         y=self.spriteHidingPlace.y, batch=batch)
        self.invertedRocketSprite.rotation = 180




    def update(self, dt):
        #Remove all the destroyed bullets from the list
        newBulletList = []
        for bullet in self.bullets:
            if not bullet.destroyed:
                bullet.update(dt)
                newBulletList.append(bullet)

            else:
                del bullet

        self.bullets = newBulletList

        self.acceleration.y = self.gravity
        self.velocity.y += self.acceleration.y * dt

        self.sprite.y += self.velocity.y * dt + 0.5 * self.acceleration.y * dt * dt

        if self.sprite.y - self.halfHeight < 0:
            self.sprite.y = 0 + self.halfHeight
            self.velocity.y = 0

        elif self.sprite.y + self.halfHeight > self.windowSize.height:
            self.sprite.y = self.windowSize.height - self.halfHeight
            self.velocity.y = 0

        #Set 'enter' to flip gravity
        if self.key_handler[key.ENTER] and self.allowKeypress[key.ENTER]:
            self.gravity = -self.gravity
            self.velocity.y = 0

            self.allowKeypress[key.ENTER] = False

        elif not self.key_handler[key.ENTER] and not self.allowKeypress[key.ENTER]:
            self.allowKeypress[key.ENTER] = True

        #Set 'space' to fire a bullet
        if self.key_handler[key.SPACE] and self.allowKeypress[key.SPACE]:
            self.fire()
            self.allowKeypress[key.SPACE] = False

        elif not self.key_handler[key.SPACE] and not self.allowKeypress[key.SPACE]:
            self.allowKeypress[key.SPACE] = True

        #Set 'right' to change weapons forwards
        if self.key_handler[key.RIGHT] and self.allowKeypress[key.RIGHT]:
            if self.equippedWeapon + 1 <= len(self.weaponList) - 1:
                self.equippedWeapon += 1
            else:
                self.equippedWeapon = 0

            self.allowKeypress[key.RIGHT] = False

        elif not self.key_handler[key.RIGHT] and not self.allowKeypress[key.RIGHT]:
            self.allowKeypress[key.RIGHT] = True

        #Set 'left' to change weapons backwards
        if self.key_handler[key.LEFT] and self.allowKeypress[key.LEFT]:
            if self.equippedWeapon - 1 >= 0:
                self.equippedWeapon -= 1
            else:
                self.equippedWeapon = len(self.weaponList) - 1

            self.allowKeypress[key.LEFT] = False

        elif not self.key_handler[key.LEFT] and not self.allowKeypress[key.LEFT]:
            self.allowKeypress[key.LEFT] = True

        if self.key_handler[key.UP]:
            self.velocity.y += self.jetpackPower
            self.rocketSprite.x = self.sprite.x
            self.rocketSprite.y = self.sprite.y - self.halfHeight - (self.rocketSprite.height / 2)

        else:
            self.rocketSprite.x = self.spriteHidingPlace.x
            self.rocketSprite.y = self.spriteHidingPlace.y

        if self.key_handler[key.DOWN]:
            self.velocity.y -= self.jetpackPower
            self.invertedRocketSprite.x = self.sprite.x
            self.invertedRocketSprite.y = self.sprite.y + self.halfHeight + (self.invertedRocketSprite.height / 2)

        else:
            self.invertedRocketSprite.x = self.spriteHidingPlace.x

            self.invertedRocketSprite.y = self.spriteHidingPlace.y

    def fire(self):
        currentWeapon = self.weaponList[self.equippedWeapon]
        if currentWeapon == "pistol":
            self.bullets.append(PlayerBullet(self.sprite.x, self.sprite.y, self.sprite.batch, self.windowSize, self))

        elif currentWeapon == "cannon":
            self.bullets.append(PlayerCannonball(self.sprite.x, self.sprite.y, self.sprite.batch, self.windowSize, self))

        elif currentWeapon == "rocket":
            self.bullets.append(PlayerRocket(self.sprite.x, self.sprite.y, self.sprite.batch, self.windowSize, self))

@PendingDeprecationWarning
class TileMapSection(object):
    def __init__(self, data, width, windowSize, value=None):
        """
        If value is specified, the random treasure-placer will place treasure to that value.
        """
        self.data = data
        self.width = width
        self.value = value

        self.x = windowSize.width + self.width / 2

        self.boundingLine = boundingShapes.BoundingLine(self.x, self.width)

        if self.value is not None:
            self.generateTreasure()

    def generateTreasure(self):
        pass


class TileMap(object):
    def __init__(self, windowBox, batch):
        #The keys for the dictionary is the column number that you want to access.
        self.data = {}
        sectionFile = shelve.open("sections")
        self.sectionChoices = [sectionFile.values()]

        self.tileSize = 128

        self.batch = batch

        self.windowBox = windowBox

        self.scrollSpeed = 500

    def update(self, dt):
        for section in self.data.keys():
            #Test if the section has gone off the screen
            if self.data[section]["boundingLine"].right.x <= 0:
                del self.data[section]
                #Now randomly choose a new section
                self.data[len(self.data.keys()) + 1] = random.choice(self.sectionChoices)

            else:
                moveValue = self.scrollSpeed * dt
                for tile in self.data[section]:
                    tile.x -= moveValue


class SoundQueue(object):
    """
    TODO:
     - Add the ability to make a sound play when another sound has finished playing
     - Make the keys an identifier rather than the sound to play
    """
    def __init__(self):
        self.currentTime = 0
        self.sounds = {}

        #self.currentSound =

    def addSound(self, sound, delay, volume, playTime=-1.0, continuous=False):
        """
        Parameters:

        delay: the delay before the sound starts playing

        playTime: the amount of time (in seconds) that the sound will play for (-1 will play for the entire duration, if continuous
        is set to true, this parameter is ignored)

        continuous: if set to true, the sound will continue looping/playing until a signal is given for it to stop
        """
        #self.sounds[]
        self.sounds[sound] = {"delay" : self.currentTime + delay, "volume" : volume, "playTime" : playTime, "continuous" : continuous}

    def deleteSound(self, sound):
        del self.sounds[sound]

    def update(self, dt):
        self.currentTime += dt
        for sound in self.sounds.keys():
            if sound["continuous"]:
                sound.play()

            else:
                if self.currentTime >= self.sounds[sound]["delay"]:
                    sound.play()
                    del self.sounds[sound]

        if len(self.sounds.keys()) == 0:
            self.currentTime = 0
