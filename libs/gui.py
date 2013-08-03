from boundingShapes import Rectangle as Rect
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





