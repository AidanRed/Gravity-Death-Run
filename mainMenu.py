import pyglet
import random
import shelve
from libs.gui import Button
from libs import simpleLibrary
from pyglet.gl import *

SEPARATOR = simpleLibrary.SEPARATOR
windowWidth = 640
windowHeight = 480
gameWindow = pyglet.window.Window(windowWidth, windowHeight)
FPS = 60
squareSize = 32


#Load all sprites/images
imgNewGameSelected = pyglet.image.load("resources" + SEPARATOR + "menu" + SEPARATOR + "menuNewGameSelected.png")
imgNewGameUnselected = pyglet.image.load("resources" + SEPARATOR + "menu" + SEPARATOR + "menuNewGameUnselected.png")
butNewGame = Button(imgNewGameUnselected, imgNewGameSelected, imgNewGameSelected.width, imgNewGameSelected.height,
                    (10, 10))


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
        #Shade. random number to start with, gradually increases to 255 then after a pause returns to 0 and gradually increases again
        self.shade = 1

    def drawSelf(self):
        pyglet.graphics.draw(4, GL_QUADS, ('v2i', (
            self.x, self.y + self.height, self.x + self.width, self.y + self.height, self.x + self.width, self.y,
            self.x, self.y)), ('c3B', (int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                       int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),)))

#Shelve stuff for settings
def changeSetting(file,key,val):
    shelf = shelve.open(file)
    shelf[key] = val
    shelf.close()

def readSetting(file,key):
    shelf = shelve.open(file)
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
        print str(i.colour)

@gameWindow.event
def on_draw():
    gameWindow.clear()
    for square in squares:
        square.drawSelf()
    butNewGame.draw()

def update(dt):
    for i in squares:
        i.colour[0] -= 0.2
        i.colour[1] -= 0.2
        i.colour[2] -= 0.2

@gameWindow.event
def on_mouse_press(x, y, button, modifiers):
    global mouseButtonPressed

    if button == pyglet.window.mouse.LEFT:
        if butNewGame.update(x, y):
            print "print"

@gameWindow.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if butNewGame.pressed:
            butNewGame.pressed = False




pyglet.clock.schedule_interval(update, 1.0 / 120.0)
pyglet.app.run()