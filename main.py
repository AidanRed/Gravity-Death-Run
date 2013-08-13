import pyglet
import engine
from libs import simpleLibrary
from libs.boundingShapes import Rectangle


def centreImage(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

window = pyglet.window.Window(1300, 600)

playerImage = pyglet.image.load("resources" + simpleLibrary.SEPARATOR + "playerImage.png")
centreImage(playerImage)

batch1 = pyglet.graphics.Batch()

player1 = engine.Player(window.width / 5, window.height / 2, playerImage, batch1, engine.Size(window.width, window.height))

window.push_handlers(player1.key_handler)

weaponLabel = pyglet.text.Label(color=(0, 255, 0, 255), batch=batch1)
weaponLabel.text = player1.weaponList[player1.equippedWeapon]

tileMap = engine.TileMap(Rectangle(window.width / 2, window.height / 2, window.width, window.height), batch1)

backgroundColour = (0, 0.11993458956850283094850680009999999999999999, 0, 1.0)
pyglet.gl.glClearColor(*backgroundColour)

@window.event
def on_draw():
    window.clear()
    batch1.draw()


def update(dt):
    player1.update(dt)
    if weaponLabel.text != player1.equippedWeapon:
        weaponLabel.text = player1.weaponList[player1.equippedWeapon]

    ##tileMap.update(dt)


pyglet.clock.schedule_interval(update, 1.0 / 120.0)
pyglet.app.run()