from vectors import Vector2
import math


class Rectangle(object):
    def __init__(self, centrePoint, width, height):
        self.id = "rectangle"

        try:
            self.x = centrePoint.x
            self.y = centrePoint.y

        except AttributeError:
            self.x = centrePoint[0]
            self.y = centrePoint[1]

        self.width = width
        self.height = height

        self.topLeft = Vector2(self.x - self.width, self.y + self.height)
        self.bottomRight = Vector2(self.x + self.width, self.y - self.height)

    def pointInside(self, point):
        try:
            pointX = point.x
            pointY = point.y

        except AttributeError:
            pointX = point[0]
            pointY = point[1]

        if pointX > self.topLeft.x and pointX < self.bottomRight.x and pointY > self.bottomRight.y and pointY < self.topLeft.y:
            return True

        else:
            return False

    def collides(self, otherShape):
        if otherShape.id == "rectangle":
            #Do rectangle vs rectangle collision
            if otherShape.topLeft.x > self.bottomRight.x:
                return False
            elif otherShape.bottomRight.x < self.topLeft.x:
                return False
            elif otherShape.topLeft.y < self.bottomRight.y:
                return False
            elif otherShape.bottomRight.y > self.topLeft.y:
                return False

            else:
                return True

        elif otherShape.id == "circle":
            #Test each edge against the circle, and see if the centre of the circle is inside the rectangle
            if self.pointInside(otherShape.middlePoint):
                return True

            elif otherShape.collidesWithLine((self.topLeft, Vector2(self.bottomRight.x, self.topLeft.y))):
                return True

            elif otherShape.collidesWithLine(Vector2(self.bottomRight.x, self.topLeft.y), self.bottomRight):
                return True

            elif otherShape.collidesWithLine(self.bottomRight, Vector2(self.topLeft.x, self.bottomRight.y)):
                return True

            elif otherShape.collidesWithLine(Vector2(self.topLeft.x, self.bottomRight.y), self.topLeft):
                return True

            else:
                return False


class Circle(object):
    def __init__(self, middlePoint, radius):
        self.id = "circle"

        #If the middlePoint is not provided as a vector, make it one
        try:
            middlePoint.id
            self.middlePoint = middlePoint

        except AttributeError:
            self.middlePoint = Vector2(middlePoint[0], middlePoint[1])

        self.x = self.middlePoint.x
        self.y = self.middlePoint.y

        self.radius = radius

    def pointInside(self, point):
        try:
            point.id
            pointX = point.x
            pointY = point.y

        except AttributeError:
            pointX = point[0]
            pointY = point[1]

        distance = math.hypot(pointX - self.x, pointY - self.y)

        if distance < self.radius:
            return True

        else:
            return False

    def collidesWithLine(self, line):
        point1 = line[0]
        point2 = line[1]

        try:
            point1.id
            point2.id

        except AttributeError:
            point1 = Vector2(point1[0], point1[1])
            point2 = Vector2(point2[0], point2[1])

        #Point1 has to be 0 in order to turn the other point into a vector that we can use
        editedPoint = point2.subtract(point1)
        editedMiddle = self.middlePoint.subtract(point1)

        projection = editedMiddle.projection(editedPoint)
        newProjection = projection.add(point1)

        if self.pointInside(newProjection):
            return True
        else:
            return False


class BoundingLine(object):
    def __init__(self, middleX, width):
        self.x = middleX
        self.width = width
        self.halfWidth = self.width / 2

        self.rightPoint = Vector2(self.x + self.width, 0)
        self.leftPoint = Vector2(self.x - self.width, 0)

    def pointInside(self, point):
        try:
            point.id
        except AttributeError:
            point = Vector2(point[0], point[1])

        if point.x < self.x + self.halfWidth and point.x > self.x - self.halfWidth:
            return True
        else:
            return False

    def intersection(self, otherLine):
        """
        Returns intersection between self and another bounding line as a bounding line
        """
        if otherLine.pointInside(self.leftPoint):
            theWidth = otherLine.rightPoint.x - self.leftPoint.x
            return BoundingLine(self.leftPoint.x + theWidth / 2, theWidth)

        elif otherLine.pointInside(self.rightPoint):
            theWidth = self.rightPoint.x - otherLine.leftPoint.x
            return BoundingLine(otherLine.leftPoint.x + theWidth / 2, theWidth)

        elif self.leftPoint.x <= otherLine.leftPoint.x and self.rightPoint.x >= otherLine.rightPoint.x:
            return BoundingLine(otherLine.x, otherLine.width)

        else:
            return False

    def rectangleIntersection(self, rectangle):
        """
        returns the intersection between self and a rectangle as a bounding line
        """
        rectangleLine = BoundingLine(rectangle.bottomRight.x - rectangle.width / 2, rectangle.width)

        return self.intersection(rectangleLine)