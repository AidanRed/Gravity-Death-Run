import pyglet
import random
import shelve
from libs.gui import TextButton
from libs import simpleLibrary
from pyglet.gl import *

#constants
SEPARATOR = simpleLibrary.SEPARATOR

#variables
windowWidth = 640
windowHeight = 480
gameWindow = pyglet.window.Window(windowWidth, windowHeight)
FPS = 60
squareSize = 64
colourChange = 3
#This string defines which screen is active. This will either be 'main', 'settings', or 'high-scores'
screen = "main"


def loadImage(mpath):
    return pyglet.image.load("resources" + SEPARATOR + "menu" + SEPARATOR + mpath)

buttonSettings = TextButton("Settings", (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (100, 0, 255), (100, 0, 255),
                            (100, 0, 255), (100, 0, 255), (0, 255, 0), (255, 255, 255), 64, 32, (640 - 74, 52), (10, 5))

buttonNewGame = TextButton("New Game", (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (100, 0, 255), (100, 0, 255),
                        (100, 0, 255), (100, 0, 255), (0, 255, 0), (255, 255, 255), 64, 32, (74, 52), (10, 5))

buttonResolution640_480 = TextButton("640*480", (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255),(100, 0, 255), (100, 0, 255),
                            (100, 0, 255), (100, 0, 255),(0, 255, 0), (255, 255, 255), 48, 16, (64, 192), (0, 0))

class Square:
    """
    Squares to be drawn on-screen in the background.
    """

    def __init__(self, x, y, height, width, columnColour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        #colour. Originally set to universal colour (for the column the square belongs to)
        self.colour = columnColour
        self.colourDirection = "-"

    def drawSelf(self):
        pyglet.graphics.draw(4, GL_QUADS, ('v2i', (
            self.x, self.y + self.height, self.x + self.width, self.y + self.height, self.x + self.width, self.y,
            self.x, self.y)), ('c3B', (int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),)))

#Shelve stuff for settings
def changeSetting(filename,key,val):
    shelf = shelve.open(filename)
    shelf[key] = val
    shelf.close()

def readSetting(filename,key):
    shelf = shelve.open(filename)
    setting = shelf[key]
    shelf.close()
    return setting



#Create the squares and set them to a grid constrained to the screen size.
squares = []
for i in range(int(windowWidth / squareSize)):
    for ii in range(int(windowHeight / squareSize)):
        squares.append(Square(i * squareSize, ii * squareSize, squareSize, squareSize, (56, 57, 58)))

#This method of setting colours for columns may be deemed inefficient and may not be used.
#Choose the colours from a list of colours. 

lblue = [51, 255, 255]
blue = [0, 0, 255]
dblue = [0, 0, 102]
red = [255, 0, 0]
pink = [255, 51, 153]
purple = [153, 51, 255]
lgreen = [204, 255, 0]
green = [51, 255, 0]
dgreen = [0, 102, 0]
yellow = [255, 255, 255]
orange = [153, 255, 51]

colours = [lblue, blue, dblue, red, pink, purple, green, dgreen, lgreen, yellow, orange]

#Determine a random colour to give to each column
possibleColours = []
for i in range(int(windowWidth / squareSize)):
    possibleColours.append(colours[random.randint(0, 10)])

for i in range(int(windowWidth / squareSize)):
    for ii in squares:
        if i * squareSize == ii.x:
            ii.colour = possibleColours[i]

#Determine slight variations in colour for each square.

for i in squares:
        i.colour = [i.colour[0]+random.randint(1,50),i.colour[1]+random.randint(1,50),i.colour[2]+random.randint(1,50)]

@gameWindow.event
def on_draw():
    gameWindow.clear()
    for square in squares:
        square.drawSelf()
    if screen == "main":
        buttonNewGame.draw()
        buttonSettings.draw()
    if screen == "settings":
        buttonResolution640_480.draw()

def update(dt):
    for i in squares:
        if i.colour[0] <= colourChange:
            if i.colourDirection != "-":
                i.colourDirection = "+"
                i.colour[0] -= colourChange
        elif i.colour[0] >= 255-colourChange:
            if i.colourDirection != "+":
                i.colourDirection = "-"
                i.colour[0] += colourChange
        if i.colour[1] <= colourChange:
            if i.colourDirection != "-":
                i.colourDirection = "+"
                i.colour[1] -= colourChange
        elif i.colour[1] >= 255-colourChange:
            if i.colourDirection != "+":
                i.colourDirection = "-"
                i.colour[1] += colourChange
        if i.colour[2] <= colourChange:
            if i.colourDirection != "-":
                i.colourDirection = "+"
                i.colour[2] -= colourChange
        elif i.colour[2] >= 255-colourChange:
            if i.colourDirection != "+":
                i.colourDirection = "-"
                i.colour[2] += colourChange

@gameWindow.event
def on_mouse_press(x, y, button, modifiers):
    global mouseButtonPressed
    global screen
    if button == pyglet.window.mouse.LEFT:
        if screen == "main":
            if buttonNewGame.update(x, y):
                pass
            elif buttonSettings.update(x, y):
                screen = "settings"
        if screen == "settings":
            if buttonResolution640_480.update(x, y):
                changeSetting("settings.dat","resolutionWidth",640)
                changeSetting("settings.dat","resolutionHeight",480)

@gameWindow.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if screen == "main":
            if buttonNewGame.pressed:
                buttonNewGame.pressed = False
            if buttonSettings.pressed:
                buttonSettings.pressed = False
        if screen == "settings":
            if buttonResolution640_480.pressed:
                buttonResolution640_480.pressed = False




pyglet.clock.schedule_interval(update, 1.0 / 30.0)
pyglet.app.run()