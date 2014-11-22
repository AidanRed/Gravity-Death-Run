import pyglet
import shelve
from libs import boundingShapes
from libs import gui
from pyglet.gl import *
from libs import simpleLibrary
from libs import vectors

TextButton = gui.TextButton
SEPARATOR = simpleLibrary.SEPARATOR
makeListInt = simpleLibrary.makeListInt
Vector2 = vectors.Vector2

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
        for i in range(int(2 * self.gridWidth / self.xSpacing)):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (i * self.xSpacing, self.y,
                                                                 i * self.xSpacing, self.y + self.gridHeight)))
        for i in range(int(self.gridHeight / self.ySpacing)):
            if i > 3:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.x, i * self.ySpacing,
                                                                     2 * (self.x + self.gridWidth), i * self.ySpacing)))


dirtBase1 = pyglet.image.load(RESOURCEPATH + "dirtBase1.png")

batch1 = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

prevID = 0


class Terrain(object):
    def __init__(self, img, x, y):
        global prevID

        self.id = prevID + 1
        prevID += 1

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
                if self.spr.y > 96:
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
sectionHeight = 448
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

GUITerrainButtons.append(TextButton("", buttonColour1, buttonColour1, buttonColour1, buttonColour1, buttonColour2,
                                 buttonColour2, buttonColour2, buttonColour2, (0, 0, 0), (0, 0, 0), 64, 64, (160, 96),
                                 (23, 16), border=(0, 1, 0, 1), borderPressed=(0, 1, 0, 1), image=dirtBase1))

SaveButton = TextButton("Save", buttonColour1, buttonColour1, buttonColour1, buttonColour1, buttonColour2, buttonColour2,
                        buttonColour2, buttonColour2, (0,0,0), (0, 0, 0), 128, 64, (window.width - 64, 32,), (23, 16),
                        border=(0, 1, 0, 1), borderPressed=(0, 1, 0, 1))

tileWidth = 32
tileHeight = 32

selectionBar = DrawableRectangle(0, 0, 128, width, (60, 50, 40))
glClearColor(0.06, 0.04, 0.5, 1)
grid = Grid(32, 32, sectionWidth, sectionHeight)

objects = []

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


class TerrainHolder(object):
    def __init__(self, tileWidth, tileHeight):
        self.data = {}
        for x in range(int(window.width / tileWidth)):
            self.data[x] = {}
            for y in range(int(window.height - 128 / tileHeight)):
                self.data[x][y] = None

        self.tileWidth = tileWidth
        self.tileHeight = tileHeight

    def placeTile(self, tile, gridX, gridY):
        tile.x = gridX * tileWidth
        tile.y = (gridY * tileHeight) + 128

        self.data[gridX][gridY] = tile

    def addColumn(self):
        self.data[max(self.data.keys())] = {}

    def moveTile(self, startPos, endPos):
        theTile = self.data[startPos[0]][startPos[1]]
        self.data[endPos[0]][endPos[1]] = theTile

        del self.data[startPos[0]][startPos[1]]

    def deleteTile(self, gridX, gridY):
        self.data[gridX][gridY] = None

    def getBoundingLine(self, leftSideX):
        width = max(makeListInt(self.data.keys())) * self.tileWidth
        return boundingShapes.BoundingLine(leftSideX * width/2, width)

terrainMap = TerrainHolder(tileWidth, tileHeight)


def save():
    """
    This maybe should be adapted to use the tile holder class
    """
    #Now save it in a shelve
    saveFile = shelve.open("sections.dat")

    try:
        newSection = str(max(makeListInt(saveFile.keys())) + 1)

    except ValueError:
        newSection = "1"

    saveFile[newSection] = {}

    for tile in objects:
        assert not tile.selected
        #First remove the offset
        tile.spr.x -= xOffset * tileWidth

        try:
            newKey = str(max(makeListInt(saveFile[newSection].keys())) + 1)

        except ValueError:
            #There are currently no sections
            newKey = "1"


        tempVar = saveFile[newSection]
        tempVar[newKey] = tile.spr
        saveFile.sync()

    v = saveFile[newSection]
    v["boundingLine"] = terrainMap.getBoundingLine(0)

    saveFile.close()


def coordinatesToGrid(x, y):
    return x / tileWidth, (y - 128) / tileHeight


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

    SaveButton.draw()
    batch1.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        for object1 in objects:
            firstSelected = object1.selected
            object1.update(x, y, mousePressed=True)
            if firstSelected:
                gridX, gridY = coordinatesToGrid(object1.spr.x, object1.spr.y)
                if gridX >= 0 and gridY >= 0:
                    terrainMap.placeTile(object1, gridX, gridY)
                    newObj = Terrain(dirtBase1, window.width / -2, window.height / -2)
                    newObj.selected = True
                    objects.append(newObj)
                    break

        objectSelected = False
        for object1 in objects:
            if object1.selected:
                objectSelected = True

        for GUIbutton in GUITerrainButtons:
            if GUIbutton.update(x, y):
                if not objectSelected:
                    newObj = Terrain(dirtBase1, window.width / -2, window.height / -2)
                    newObj.selected = True
                    objects.append(newObj)

        if SaveButton.update(x, y):
            if not objectSelected:
                save()

    if button == pyglet.window.mouse.RIGHT:
        gridX, gridY = coordinatesToGrid(x, y)
        if not (gridX < 0 or gridY < 0):
            if terrainMap.data[gridX][gridY] is not None:
                theTileID = terrainMap.data[gridX][gridY].id
                terrainMap.deleteTile(gridX, gridY)

                for index, value in enumerate(objects):
                    if value.id == theTileID:
                        del objects[index]


@window.event
def on_mouse_motion(x, y, dx, dy):
    for object1 in objects:
        object1.update(x, y)

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
        terrainMap.addColumn()
        for tile in objects:
            tile.spr.x -= tileWidth

    backStripOffset = xOffset % 2

pyglet.app.run()