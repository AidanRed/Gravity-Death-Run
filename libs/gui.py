from boundingShapes import Rectangle as Rect
from boundingShapes import Circle
import pyglet
from simpleLibrary import SEPARATOR
from vectors import Vector2


class Button(object):
    """
    A simple button object. Uses a bounding box for testing if it is clicked.
    """
    def __init__(self, image, imagePressed, width, height, xy):
        """
        Parameters:

        width: The width of the button

        height: The height of the button

        xy: A 2-element tuple containing the x and y coordinate of the bottom left corner of the button
        """
        self.rectangle = Rect(xy,width,height)
        self.image = image
        self.imagePressed = imagePressed

        self.x = xy[0]
        self.y = xy[1]

        self.pressed = False

    def update(self, mouseX, mouseY):
        self.pressed = self.rectangle.pointInside((mouseX,mouseY))
        return self.pressed

    def draw(self):
        if self.pressed:
            self.imagePressed.blit(self.x, self.y)

        elif not self.pressed:
            self.image.blit(self.x, self.y)


class TextButton(object):
    def __init__(self, text, colour, colour2, colour3, colour4, colourPressed, colourPressed2, colourPressed3,
                 colourPressed4, textColour, textColourPressed, width, height, xy, padding, filled=True, border=None,
                 borderPressed=None, font=None, fontSize=10, bold=False, italic=False, image=None):

#        assert (border is None and borderPressed is None) or (border is not None and borderPressed is not None)

        if len(colour) == 3:
            colour = (colour[0], colour[1], colour[2], 255)

        if len(colour2) == 3:
            colour2 = (colour2[0], colour2[1], colour2[2], 255)

        if len(colour3) == 3:
            colour3 = (colour3[0], colour3[1], colour3[2], 255)

        if len(colour4) == 3:
            colour4 = (colour4[0], colour4[1], colour4[2], 255)

        if len(colourPressed) == 3:
            colourPressed = (colourPressed[0], colourPressed[1], colourPressed[2], 255)

        if len(colourPressed2) == 3:
            colourPressed2 = (colourPressed2[0], colourPressed2[1], colourPressed3[2], 255)

        if len(colourPressed3) == 3:
            colourPressed3 = (colourPressed3[0], colourPressed3[1], colourPressed3[2], 255)

        if len(colourPressed4) == 3:
            colourPressed4 = (colourPressed4[0], colourPressed4[1], colourPressed4[2], 255)

        if len(textColour) == 3:
            textColour = (textColour[0], textColour[1], textColour[2], 255)

        if len(textColourPressed) == 3:
            textColourPressed = (textColourPressed[0], textColourPressed[1], textColourPressed[2], 255)


        self.rectangle = Rect(xy, width, height)
        self.label = pyglet.text.Label(text, font, fontSize, bold, italic, textColour, xy[0] + padding[0], xy[1] - padding[1], width - padding[0], height - padding[1],
                                       anchor_x='center', anchor_y='center', halign='center', multiline=True)

        self.colour = colour
        self.colour2 = colour2
        self.colour3 = colour3
        self.colour4 = colour4

        self.colourPressed = colourPressed
        self.colourPressed2 = colourPressed2
        self.colourPressed3 = colourPressed3
        self.colourPressed4 = colourPressed4

        self.textColour = textColour
        self.textColourPressed = textColourPressed

        self.filled = filled

        self.border = border
        self.borderPressed = borderPressed

        self.image = image

        self.pressed = False

    def setText(self, text):
        self.label.text = text

    def update(self, mouseX, mouseY):
        self.pressed = self.rectangle.pointInside((mouseX, mouseY))
        return self.pressed

    def draw(self):
        if not self.pressed:
            pyglet.gl.glColor4f(self.colour[0], self.colour[1], self.colour[2], self.colour[3])
            if self.label.color == self.colourPressed:
                self.label.color = self.colour

        else:
            pyglet.gl.glColor4f(self.colourPressed[0], self.colourPressed[1], self.colourPressed[2], self.colourPressed[3])
            if self.label.color == self.colour:
                self.label.color = self.colourPressed

        if self.filled:
            if not self.pressed:

                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (
                    int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y), int(self.rectangle.bottomRight.x),
                    int(self.rectangle.bottomRight.y), int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y),
                    int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y))), ('c3B', (int(self.colour[0]), int(self.colour[1]), int(self.colour[2]),
                                               int(self.colour2[0]), int(self.colour2[1]), int(self.colour2[2]),
                                               int(self.colour3[0]), int(self.colour3[1]), int(self.colour3[2]),
                                               int(self.colour4[0]), int(self.colour4[1]), int(self.colour4[2]),)))

            else:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (
                    int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y), int(self.rectangle.bottomRight.x),
                    int(self.rectangle.bottomRight.y), int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y),
                    int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y))), ('c3B', (int(self.colourPressed[0]), int(self.colourPressed[1]), int(self.colourPressed[2]),
                                                                   int(self.colourPressed2[0]), int(self.colourPressed2[1]), int(self.colourPressed2[2]),
                                                                   int(self.colourPressed3[0]), int(self.colourPressed3[1]), int(self.colourPressed3[2]),
                                                                   int(self.colourPressed4[0]), int(self.colourPressed4[1]), int(self.colourPressed4[2]),)))

            if self.border != None:
                if self.pressed:
                    pyglet.gl.glColor4f(*self.borderPressed)
                else:
                    pyglet.gl.glColor4f(*self.border)

                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y),
                                                                     int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y))))

                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y),
                                                                     int(self.rectangle.bottomRight.x), int(self.rectangle.bottomRight.y))))

                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.bottomRight.x), int(self.rectangle.bottomRight.y),
                                                                     int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y))))

                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y),
                                                                     int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y))))



        else:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y),
                                                                 int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y))))

            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.bottomRight.x), int(self.rectangle.topLeft.y),
                                                                 int(self.rectangle.bottomRight.x), int(self.rectangle.bottomRight.y))))

            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.bottomRight.x), int(self.rectangle.bottomRight.y),
                                                                 int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y))))

            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.rectangle.topLeft.x), int(self.rectangle.bottomRight.y),
                                                                 int(self.rectangle.topLeft.x), int(self.rectangle.topLeft.y))))
        if self.image is not None:
            pyglet.gl.glColor4f(1, 1, 1, 1)
            self.image.blit(self.rectangle.x - self.image.width / 2, self.rectangle.y - self.image.height / 2)

        self.label.draw()


class Slider(object):
    def __init__(self, leftPoint, rightPoint, startingValue, maxValue, minValue, batch, colour=(0, 0, 255, 255)):
        try:
            leftPoint.id
            rightPoint.id

            self.leftPoint = leftPoint
            self.rightPoint = rightPoint

        except AttributeError:
            self.leftPoint = Vector2(leftPoint[0], leftPoint[1])
            self.rightPoint = Vector2(rightPoint[0], rightPoint[1])

        assert startingValue <= maxValue and startingValue >= minValue

        self.length = self.rightPoint.x - self.leftPoint.x

        self.maxValue = maxValue
        self.minValue = minValue

        self.currentValue = startingValue
        sliderImage = pyglet.image.load("../resources" + SEPARATOR + "gui" + SEPARATOR + "sliderHandle.png")
        sliderImage.anchor_y = sliderImage.height / 2
        sliderImage.anchor_x = sliderImage.width / 2

        self.sliderHandle = pyglet.sprite.Sprite(sliderImage, batch=batch)
        self.sliderHandle.x = self.leftPoint.x + startingValue
        self.sliderHandle.y = self.leftPoint.y

        self.colour = colour

        self.boundingCircle = Circle((self.sliderHandle.x, self.sliderHandle.y), sliderImage.width / 2)

        self.beingPressed = False

    def draw(self):
        pyglet.gl.glColor4f(*self.colour)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (int(self.leftPoint.x), int(self.leftPoint.y), int(self.rightPoint.x), int(self.rightPoint.y))))

    def checkPressed(self, mouseX, mouseY):
        if self.boundingCircle.pointInside((mouseX, mouseY)):
            self.beingPressed = True

    def update(self, mouseX, mouseY):
        if self.beingPressed:
            if mouseX > self.rightPoint.x:
                self.sliderHandle.x = self.rightPoint.x

            elif mouseX < self.leftPoint.x:
                self.sliderHandle.x = self.leftPoint.x

            else:
                self.sliderHandle.x = mouseX


def test():
    window = pyglet.window.Window(640, 480)

    batch1 = pyglet.graphics.Batch()

    slider = Slider((20, 240), (120, 240), 1, 100, 1, batch1)

    @window.event
    def on_draw():
        window.clear()
        slider.draw()
        batch1.draw()


    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if (buttons & pyglet.window.mouse.LEFT) and not slider.beingPressed:
            slider.checkPressed(x, y)

        if (buttons & pyglet.window.mouse.LEFT) and slider.beingPressed:
            slider.update(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and slider.beingPressed:
            slider.beingPressed = False


    pyglet.app.run()