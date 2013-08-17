"""
Contains a simple 2d vector class
"""
import math

#Precision is how small the number can get before it is just changed to 0
PRECISION = 0.00000001


class Vector2(object):
    """
    Simple 2d vector class
    """

    def __init__(self, x, y, startingPoint=None):
        """
        Parameters:

        x: The x coordinate of the vector (integer)

        y: The y coordinate of the vector (integer)

        startingPoint: The starting point of the vector
        """
        self.id = "vector2"

        if startingPoint != None:
            try:
                self.x = float(x - startingPoint.x)
                self.y = float(y - startingPoint.y)

            except:
                self.x = float(x - startingPoint[0])
                self.y = float(y - startingPoint[1])

        else:
            self.x = float(x)
            self.y = float(y)

    def zero(self):
        """
        Makes the x and y coordinates of the vector 0
        """
        self.x = 0
        self.y = 0

        return self

    def clone(self):
        """
        Returns an exact copy of self
        """

        return Vector2(self.x, self.y)

    def dotProduct(self, otherVector):
        """
        Gets the dot product between self and another vector
        """

        return (self.x * otherVector.x) + (self.y * otherVector.y)

    def getAngle(self):
        """
        Gets the angle of self
        """

        return math.atan2(self.y, self.x)

    def angleBetween(self, otherVector):
        """
        Gets the angle between self and another vector

        Parameters:

        otherVector: The other vector to test against
        """
        if not self.isNormalized():
            vector1 = self.clone().normalize()
        else:
            vector1 = self

        if not otherVector.isNormalized():
            vector2 = self.clone().normalize()
        else:
            vector2 = otherVector

        return float(math.acos(vector1.dotProduct(vector2)))

    def projection(self, otherVector):
        """
        Returns the projection of self onto the other vector

        Parameters:

        otherVector: The vector to project onto
        """

        dotProduct = otherVector.dotProduct(otherVector)
        if 0 < dotProduct:
            newDotProduct = self.dotProduct(otherVector)
            return otherVector.multiply(newDotProduct / dotProduct)

        else:
            return dotProduct


    def normalize(self):
        """
        Makes the length of the vector equal to 1
        """

        length = self.getLength()

        self.x /= length
        self.y /= length

        return self

    def perpendicular(self):
        """
        Returns a vector perpendicular to this vector
        """

        return Vector2(self.y, -self.x)

    def add(self, otherVector):
        """
        Adds the x component of self and the other vector's x, and adds the y component of self and the other vector's y
        """
        newVector = Vector2(self.x + otherVector.x, self.y + otherVector.y)

        return newVector

    def subtract(self, otherVector):
        """
        Subtracts the x component of self and the other vector's x, and adds the y component of self and the other vector's y
        """
        newVector = Vector2(self.x - otherVector.x, self.y - otherVector.y)

        return newVector

    def isZero(self):
        """
        Returns True if x and y coordinates of self are 0
        """

        return self.x == 0 and self.y == 0

    def isNormalized(self):
        """
        Returns True if self is normalized (x and y are equal to 1)
        """
        return self.getLength() == 1

    def lengthSquared(self):
        """
        Returns self.x squared + self.y squared
        """
        return self.x * self.x + self.y * self.y

    def getLength(self):
        """
        Returns the square root of self.lengthSquared()
        """
        return math.sqrt(self.lengthSquared())

    def equals(self, otherVector):
        """
        Returns True if otherVector is in the same position as self
        """
        return self.x == otherVector.x and self.y == otherVector.y

    def setLength(self, length):
        """
        Sets the length of the vector, but keeps the angle the same

        Parameters:
        length: The required length in pixels
        """

        angle = self.getAngle()

        print angle
        print length

        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length

        if abs(self.x) < PRECISION:
            self.x = 0

        if abs(self.y) < PRECISION:
            self.y = 0

        return self

    def setAngle(self, angle):
        """
        Sets the angle of the Vector. Angle must be in radians.

        angle: The required angle in radians.
        """

        length = self.getLength()

        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length

        return self

    def truncate(self, value):
        """
        Sets the length under the given value. Nothing is done if the vector is shorter.

        value: The required length in pixels
        """

        self.setLength(min(value, self.getLength()))

        return self

    def reverse(self):
        """
        Make the vector point in the opposite direction
        """
        self.x = -self.x
        self.y = -self.y

        return self

    def crossProduct(self, otherVector):
        """
        Gets the cross-product of self and another vector

        Parameters:

        otherVector: The other vector to get the the cross product against
        """

        return self.x * otherVector.y - self.y * otherVector.x

    def sign(self, otherVector):
        """
        Returns True if otherVector is to the left, and False if it is to the right.

        Parameters:

        otherVector: The other vector to test against
        """
        dot = self.perpendicular().dotProduct(otherVector)

        if dot < 0:
            return False
        else:
            return True

    def distance(self, otherVector):
        """
        Gets the distance between self and another vector

        Parameters:

        otherVector: The other vector to test against
        """

        return math.sqrt(self.distanceSquared(otherVector))

    def distanceSquared(self, otherVector):
        """
        Gets the squared distance between vectors. Faster than distance (does not use square-root).

        Parameters:

        otherVector: The other vector to test against
        """

        deltaX = otherVector.x - self.x
        deltaY = otherVector.y - self.y

        return deltaX * deltaX + deltaY * deltaY

    def multiply(self, scalar):
        """
        Multiplies self by a scalar

        Parameters:

        scalar: The scalar quantity to multiply by
        """

        self.x *= scalar
        self.y *= scalar

        return self

    def divide(self, scalar):
        """
        Divides self by a scalar

        Parameters:

        scalar: The scalar quantity to divide by
        """

        self.x /= scalar
        self.y /= scalar

        return self

    def transform(self, matrix):
        """
        Transforms the vector using a matrix (basically just an array of numbers)

        Parameters:

        matrix: The matrix to transform by (needs to be the adapted class in simpleMaths.py)
        """
        newVector = self.clone()

        newVector.setX(self.x * matrix.a + self.y * matrix.c + matrix.tx)
        newVector.setY(self.x * matrix.b + self.y * matrix.d + matrix.ty)

        return newVector

    def reverse(self):
        """
        Make self point in the opposite direction
        """
        self.x = -self.x
        self.y = -self.y

        return self

    def polarCoordinates(self):
        """
        Converts vector coordinates into polar coordinates.
        Returns a 2-element tuple containing the length of the vector and the angle.
        """
        length = self.getLength()
        angle = self.getAngle()

        return (length, angle)

    def polarToCartesian(self, length, angle):
        """
        Converts polar coordinates back to cartesian coordinates.
        Returns a 2-element tuple containing x and y coordinates

        Parameters:

        length: The length of the vector (float)
        angle: The angle of the vector (float)
        """
        return (length * math.cos(angle), length * math.sin(angle))

    def setX(self, x):
        """
        Sets the x component of the vector

        x: The x coordinate to set (integer)
        """
        self.x = x

    def setY(self, y):
        """
        Sets the y component of the vector

        y: The y coordinate to set (integer)
        """
        self.y = y

    def gradient(self):
        """
        Calculates the gradient of the vector: rise/run
        Returns float
        """
        return self.y / self.x

    def antiGradient(self):
        """
        The opposite of the gradient: run/rise
        Returns float
        """
        return self.x / self.y

    def drawSelf(self, colour=(0, 1.0, 0, 1.0)):
        """
        draws the vector to the window provided as parameter.

        Parameters:

        (optional) colour: a 4-element tuple containing the colour that the vector is drawn, in RGBA format. (default: green)
        """

        import pyglet.gl
        import pyglet.graphics

        pyglet.gl.glColor4f(colour[0], colour[1], colour[2], colour[3])
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (0, 0, self.x, self.y)))


def test():
    """
    A simple test for the Vector2 class that makes a new vector, and then draws it to a window
    """
    import pyglet

    vector1 = Vector2(100, 100)

    window = pyglet.window.Window()

    @window.event
    def on_draw():
        vector1.drawSelf(window)

    pyglet.app.run()


def testProjection(vector1=Vector2(38, 64), vector2=Vector2(50, 0)):
    theProjection = vector1.projection(vector2)
    print theProjection

    print "x: " + str(theProjection.x)
    print "y: " + str(theProjection.y)