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
    def __init__(self, text, colour, colour2, colour3, colour4, colourPressed, colourPressed2, colourPressed3,
                 colourPressed4, textColour, textColourPressed, width, height, xy, padding, filled=True, border=None,
                 borderPressed=None, font=None, fontSize=10, bold=False, italic=False):

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
        self.label = pyglet.text.Label(text, font, fontSize, bold, italic, textColour, xy[0] + padding[0], xy[1] + padding[1], width - padding[0], height - padding[1],
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

        self.label.draw()






