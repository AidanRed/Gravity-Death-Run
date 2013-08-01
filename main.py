import pyglet
import engine


def centreImage(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

window = pyglet.window.Window(1300, 600)

playerImage = pyglet.image.load("playerImage.png")
centreImage(playerImage)

batch1 = pyglet.graphics.Batch()

player1 = engine.Player(window.width/2, window.height/2, playerImage, batch1, engine.Size(window.width, window.height))

window.push_handlers(player1.key_handler)

@window.event
def on_draw():
    window.clear()
    batch1.draw()

def update(dt):
    player1.update(dt)

pyglet.app.run()