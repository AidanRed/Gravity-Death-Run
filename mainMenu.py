import pyglet
import random
import shelve
from libs.gui import Button
from libs import simpleLibrary
from pyglet.gl import *

'''constants'''
SEPARATOR = simpleLibrary.SEPARATOR

'''variables'''
windowWidth = 640
windowHeight = 480
gameWindow = pyglet.window.Window(windowWidth, windowHeight)
FPS = 60
squareSize = 32
colourChange = 1
#This string defines which screen is active. This will either be 'main', 'settings', or 'high-scores'
screen = "main"

def loadImage(mpath):
    return pyglet.image.load("resources" + SEPARATOR + "menu" + SEPARATOR + mpath)

#Load all sprites/images
imgNewGameSelected = loadImage("menuNewGameSelected.png")
imgNewGameUnselected = loadImage("menuNewGameUnselected.png")
imgSettingsSelected = loadImage("menuSettingsSelected.png")
imgSettingsUnselected = loadImage("menuSettingsUnselected.png")
butNewGame = Button(imgNewGameUnselected, imgNewGameSelected, imgNewGameSelected.width, imgNewGameSelected.height,
                    (10, 10))
butSettings = Button(imgSettingsUnselected, imgSettingsSelected, imgSettingsSelected.width, imgSettingsSelected.height,
    (139,10))

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
    shelf.close()
    return shelf[key]



#Create the squares and set them to a grid constrained to the screen size.
squares = []
for i in range(windowWidth / squareSize):
    for ii in range(windowHeight / squareSize):
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
for i in range(windowWidth / squareSize):
    possibleColours.append(colours[random.randint(0, 10)])

for i in range(windowWidth / squareSize):
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
        butNewGame.draw()
        butSettings.draw()

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
            if butNewGame.update(x, y):
                print "print"
            elif butSettings.update(x, y):
                screen = "settings"

@gameWindow.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if screen == "main":
            if butNewGame.pressed:
                butNewGame.pressed = False




pyglet.clock.schedule_interval(update, 1.0 / 120.0)
pyglet.app.run()