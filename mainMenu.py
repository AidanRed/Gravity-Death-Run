import pyglet
import random
import simpleLibrary
from pyglet.gl import *

SEPARATOR = simpleLibrary.SEPARATOR
windowWidth = 640
windowHeight = 480
gameWindow = pyglet.window.Window(windowWidth, windowHeight)
FPS = 60
squareSize = 32

#Load all sprites/images
imgNewGameSelected = pyglet.image.load("resources"+SEPARATOR+"menu"+SEPARATOR+"menuNewGameSelected.png")
sprNewGameSelected = pyglet.sprite.Sprite(imgNewGameSelected, x=10,y=10)
imgNewGameUnselected = pyglet.image.load("resources"+SEPARATOR+"menu"+SEPARATOR+"menuNewGameUnselected.png")
sprNewGameUnselected = pyglet.sprite.Sprite(imgNewGameSelected, x=10,y=10)

#Squares to be drawn on-screen in the background. 
class Square:
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

possibleColours = []
for i in range(windowWidth / squareSize):
    possibleColours.append(colours[random.randint(0, 10)])
    print i

for i in range(windowWidth / squareSize):
    for ii in squares:
        if i * squareSize == ii.x:
            ii.colour = possibleColours[i]


@gameWindow.event
def on_draw():
    gameWindow.clear()
    for square in squares:
        square.drawSelf()


def update(dt):
    for i in squares:
        i.colour[0]+=0.1
        i.colour[1]+=0.1
        i.colour[2]+=0.1



pyglet.clock.schedule_interval(update, 1.0 / 120.0)
pyglet.app.run()