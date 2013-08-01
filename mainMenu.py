import pyglet
from pyglet.gl import *
windowWidth = 640
windowHeight = 480
gameWindow = pyglet.window.Window(width,height)
FPS = 60



#Squares to be drawn on-screen in the background. 
class square:
    def __init__(self,x,y,height,width,columnColour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        #colour. Originally set to universal colour (for the column the square belongs to)
        self.colour = colour
        #Shade. random number to start with, gradually increases to 255 then after a pause returns to 0 and gradually increases again
        self.shade = 1
        
    def drawSelf(self):
        pyglet.graphics.draw(4, GL_QUADS,('v2i', (x,y+height, x+width,y+height, x+width,y, x,y)),('c3B', (self.colour[0],self.colour[1],self.colour[2],
                                                                                                          self.colour[0],self.colour[1],self.colour[2],
                                                                                                          self.colour[0],self.colour[1],self.colour[2],
                                                                                                          self.colour[0],self.colour[1],self.colour[2],)))
        

@gameWindow.event
def on_draw():
    gameWindow.clear()
    score_label.draw()
    
def update(dt):
    score_label.draw()   
    
pyglet.clock.schedule_interval(update, 1.0/120.0)    
pyglet.app.run()