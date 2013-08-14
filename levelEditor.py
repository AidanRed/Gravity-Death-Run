import pyglet
from libs import simpleLibrary
from libs import boundingShapes
from libs.gui import TextButton
from pyglet.gl import *

class DrawableRectangle(object):
    """
    Simple class for drawing quads with opengl
    """
    def __init__(self,x,y,height,width,colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self):
        pyglet.graphics.draw(4, GL_QUADS, ('v2i', (
        self.x, self.y + self.height, self.x + self.width, self.y + self.height, self.x + self.width, self.y,
        self.x, self.y)), ('c3B', (int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                   int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                   int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                   int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),)))

class Grid(object):
    def __init__(self,xSpacing, ySpacing, gridHeight, gridWidth, x=0, y=128):
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.x = x
        self.y = y

    def draw(self):
        for i in range(2*self.gridWidth/self.xSpacing):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (i*self.xSpacing,self.y,
                i*self.xSpacing,self.y+self.gridHeight)))
        for i in range(self.gridHeight/self.ySpacing):
            if i > 3:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.x,i*self.ySpacing,
                    2*(self.x+self.gridWidth),i*self.ySpacing)))



width = 640
height = 480
window = pyglet.window.Window(width, height)
sectionWidth = width
sectionHeight = 320
glColor4f(255,4,6,2)

selectionBar = DrawableRectangle(0,0,128,width,(60,50,40))
glClearColor(0.06,0.04,0.5,1)
grid = Grid(32,32,sectionWidth,sectionHeight)
@window.event
def on_draw():
    window.clear()
    selectionBar.draw()
    grid.draw()





pyglet.app.run()