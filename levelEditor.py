import pyglet
import shelve
from libs import boundingShapes
from libs.gui import TextButton
from pyglet.gl import *
from libs.simpleLibrary import SEPARATOR
from libs.vectors import Vector2

RESOURCEPATH = "resources" + SEPARATOR + "terrain" + SEPARATOR


def snapToGrid(point, gridSize):
    return gridSize * round(point.x/gridSize), gridSize * round(point.y/gridSize)


class DrawableRectangle(object):
    """
    Simple class for drawing quads with opengl
    """


    def __init__(self, x, y, height, width, colour):
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
    def __init__(self, xSpacing, ySpacing, gridHeight, gridWidth, x=0, y=128):
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.x = x
        self.y = y


    def draw(self):
        pyglet.gl.glColor4f(1, 1, 1, 1)
        for i in range(2 * self.gridWidth / self.xSpacing):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (i * self.xSpacing, self.y,
                                                                 i * self.xSpacing, self.y + self.gridHeight)))
        for i in range(self.gridHeight / self.ySpacing):
            if i > 3:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.x, i * self.ySpacing,
                                                                     2 * (self.x + self.gridWidth), i * self.ySpacing)))


dirtBase1 = pyglet.image.load(RESOURCEPATH + "dirtBase1.png")

batch1 = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


class Terrain(object):
    def __init__(self, img, x, y):
        self.spr = pyglet.sprite.Sprite(img, x=x, y=y, batch=batch1, group=foreground)
        self.img = img
        
        self.width = self.img.width
        self.height = self.img.height

        self.rect = boundingShapes.Rectangle((x + (img.width / 2), y + (img.height / 2)), self.width, self.height)
        self.selected = False

    def mouseCollide(self, mouseX, mouseY):
        self.rect = boundingShapes.Rectangle((self.spr.x + (self.img.width / 2), self.spr.y + (self.img.height / 2)),
                                             self.img.width, self.img.height)

        return self.rect.pointInside((mouseX, mouseY))

    def update(self, mouseX, mouseY, mousePressed=False):
        self.rect = boundingShapes.Rectangle((self.spr.x + (self.img.width / 2), self.spr.y + (self.img.height / 2)),
                                             self.img.width, self.img.height)

        if mousePressed:
            if not self.selected:
                if self.rect.pointInside((mouseX, mouseY)):
                    self.selected = True

            else:
                self.selected = False

        if self.selected:
            self.spr.x, self.spr.y = snapToGrid(Vector2(mouseX - self.width / 2, mouseY - self.height / 2), self.width)


class BackgroundStrip(object):
    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, offset):
        if offset == 1:
            offset = tileWidth
        else:
            offset = 0

        pyglet.graphics.draw(4, GL_QUADS, ('v2i', (
            self.x + offset, self.y + self.height, self.x + self.width + offset, self.y + self.height, self.x + self.width + offset, self.y,
            self.x + offset, self.y)), ('c3B', (int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                        int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                        int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                        int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),)))


width = 640
height = (480+128)
window = pyglet.window.Window(width, height)
sectionWidth = width
sectionHeight = 320
glColor4f(255, 4, 6, 2)

buttonColour1 = (0, 55, 255)
buttonColour2 = (0, 105, 255)

GUILeftButtons = []
GUILeftButtons.append(TextButton("Terrain", buttonColour1, buttonColour1, buttonColour1, buttonColour1, buttonColour2,
                                 buttonColour2, buttonColour2, buttonColour2, (0, 0, 0), (0, 0, 0), 128, 64, (64, 95),
                                 (23, 16), border=(0, 1, 0, 1)))
GUILeftButtons.append(TextButton("Enemies", buttonColour1, buttonColour1, buttonColour1, buttonColour1, buttonColour2,
                                 buttonColour2, buttonColour2, buttonColour2, (0, 0, 0), (0, 0, 0), 128, 64,
                                 (64, 95 - 64), (23, 16), border=(0, 1, 0, 1)))

GUITerrainButtons = []
GUITerrainButtons.append(TextButton("Dirt?", buttonColour1, buttonColour1, buttonColour1, buttonColour1, buttonColour2,
                                 buttonColour2, buttonColour2, buttonColour2, (0, 0, 0), (0, 0, 0), 128, 64, (512, 95),
                                 (23, 16), border=(0, 1, 0, 1), borderPressed=(0, 1, 0, 1)))

tileWidth = 32
tileHeight = 32

selectionBar = DrawableRectangle(0, 0, 128, width, (60, 50, 40))
glClearColor(0.06, 0.04, 0.5, 1)
grid = Grid(32, 32, sectionWidth, sectionHeight)

objects = []
objects.append(Terrain(dirtBase1, window.width / 2, window.height / 2))

backgroundStrips = []

stripColour = ()

previousX = -(tileWidth * 2)
step = tileWidth * 2
for i in range(int((window.width / tileWidth) / 2)):
    backgroundStrips.append(BackgroundStrip((0.06, 0.04, 0.5, 1),previousX + step, 0, tileWidth, window.height))
    previousX += step

#backStripOffset can either be 0 or 1.
backStripOffset = 0

#xOffset is in tiles, not pixels
xOffset = 0


def save():
    for tile in objects:
        assert not tile.selected
        #First remove the offset
        tile.spr.x -= xOffset * tileWidth

        #Now save it in a shelve
        saveFile = shelve.open("sections.dat")
        try:
            newKey = max(saveFile.keys()) + 1

        except ValueError:
            #There are currently no sections
            newKey = 1




@window.event
def on_draw():
    window.clear()
    for backStrip in backgroundStrips:
        backStrip.draw(backStripOffset)

    grid.draw()

    selectionBar.draw()

    for button in GUILeftButtons:
        button.draw()
    for button in GUITerrainButtons:
        button.draw()
    batch1.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        for object in objects:
            object.update(x, y, mousePressed=True)
        for GUIbutton in GUITerrainButtons:
            if GUIbutton.update(x, y):
                tempVar = 0
                for object in objects:
                    if object.selected == True:
                        tempVar = 1
                if tempVar == 0:
                    newObj = Terrain(dirtBase1, window.width / -2, window.height / -2)
                    newObj.selected = True
                    objects.append(newObj)

@window.event
def on_mouse_motion(x, y, dx, dy):
    for object in objects:
        object.update(x, y)

@window.event
def on_key_press(symbol, modifiers):
    global xOffset, objects, backStripOffset

    if symbol == pyglet.window.key.LEFT:
        if xOffset > 0:
            xOffset -= 1

            for tile in objects:
                tile.spr.x += tileWidth

    elif symbol == pyglet.window.key.RIGHT:
        xOffset += 1
        for tile in objects:
            tile.spr.x -= tileWidth

    backStripOffset = xOffset % 2

pyglet.app.run()