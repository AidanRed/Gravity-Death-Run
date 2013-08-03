from boundingShapes import Rectangle as Rect
import pyglet


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
    def __init__(self, text, colour, colourPressed, textColour, textColourPressed, width, height, xy, padding, font=None, fontSize=10, bold=False, italic=False):
        if len(colour) == 3:
            colour = (colour[0], colour[1], colour[2], 255)

        if len(colourPressed) == 3:
            colourPressed = (colourPressed[0], colourPressed[1], colourPressed[2], 255)

        if len(textColour) == 3:
            textColour = (textColour[0], textColour[1], textColour[2], 255)

        if len(textColourPressed) == 3:
            textColourPressed = (textColourPressed[0], textColourPressed[1], textColourPressed[2], 255)

        self.rectangle = Rect(xy, width, height)
        self.label = pyglet.text.Label(text, font, fontSize, bold, italic, colour, xy[0], xy[1], width - padding[0], height - padding[1],
                                       anchor_x='center', anchor_y='centre', halign='centre', multiline=True)

        self.colour = colour
        self.colourPressed = colourPressed

        self.textColour = textColour
        self.textColourPressed = textColourPressed

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

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.rectangle.topLeft.x, self.rectangle.topLeft.y,
                                                             self.rectangle.bottomRight.x, self.rectangle.topLeft.y)))

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.rectangle.bottomRight.x, self.rectangle.topLeft.y,
                                                             self.rectangle.bottomRight.x, self.rectangle.bottomRight.y)))

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.rectangle.bottomRight.x, self.rectangle.bottomRight.y,
                                                             self.rectangle.topLeft.x, self.rectangle.bottomRight.y)))

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (self.rectangle.topLeft.x, self.rectangle.bottomRight.y,
                                                             self.rectangle.topLeft.x, self.rectangle.topLeft.y)))
        self.label.draw()






