import pyglet
from libs import simpleLibrary
from libs import boundingShapes
from libs.gui import TextButton
from pyglet.gl import *
from libs.simpleLibrary import SEPARATOR

RESOURCEPATH = "resources" + SEPARATOR + "terrain" + SEPARATOR

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

dirtBaseBig1 = pyglet.image.load(RESOURCEPATH + "dirtBaseBig1.png")
drawBatch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

class terrain(object):
    def __init__(self,img,x,y):
        self.spr = pyglet.sprite.Sprite(img,x=x,y=y,batch=drawBatch,group=foreground)
        self.img = img
        self.rect = boundingShapes.Rectangle((x+(img.width/2),y+(img.height/2)),img.width,img.height)

    def mouseCollide(self,mouseX,mouseY):
        self.rect = boundingShapes.Rectangle((self.spr.x+(self.img.width/2),self.spr.y+(self.img.height/2)),
                                             self.img.width,self.img.height)
        return self.rect.pointInside((mouseX,mouseY))



objects = []
objects.append(terrain(dirtBaseBig1, 444, 444))


width = 640
height = 480
window = pyglet.window.Window(width, height)
sectionWidth = width
sectionHeight = 320
glColor4f(255,4,6,2)

buttonColour1 = (0,55,255)
buttonColour2 = (0,105,255)

#List of all objects
objectList = []

#def __init__(self, text, colour, colour2, colour3, colour4, colourPressed, colourPressed2, colourPressed3,
# colourPressed4, textColour, textColourPressed, width, height, xy, padding, filled=True, font=None, fontSize=10,
# bold=False, italic=False)
#GUI objects
GUILeftButtons = []
GUILeftButtons.append(TextButton("Terrain",buttonColour1,buttonColour1,buttonColour1,buttonColour1,buttonColour2,
                                 buttonColour2,buttonColour2,buttonColour2,(0,0,0),(0,0,0),128,64,(64,95),(10,-32)))
GUILeftButtons.append(TextButton("Enemies",buttonColour1,buttonColour1,buttonColour1,buttonColour1,buttonColour2,
                                 buttonColour2,buttonColour2,buttonColour2,(0,0,0),(0,0,0),128,64,(64,95-64),(10,-32)))


selectionBar = DrawableRectangle(0,0,128,width,(60,50,40))
glClearColor(0.06,0.04,0.5,1)
grid = Grid(32,32,sectionWidth,sectionHeight)
@window.event
def on_draw():
    window.clear()
    drawBatch.draw()
    selectionBar.draw()

    grid.draw()

    for button in GUILeftButtons:
        button.draw()

@window.event
def on_mouse_motion(x,y,dx,dy):
    if objects[0].mouseCollide(x,y):
        objects[0].spr.image.anchor_x = x-objects[0].spr.y
        objects[0].spr.image.anchor_y = y-objects[0].spr.y
        objects[0].spr.x = x
        objects[0].spr.y = y





pyglet.app.run()