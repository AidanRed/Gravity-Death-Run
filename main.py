import pyglet
import engine
from libs import simpleLibrary


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

@window.event
def on_draw():
    window.clear()
    batch1.draw()


def update(dt):
    player1.update(dt)
    if weaponLabel.text != player1.equippedWeapon:
        weaponLabel.text = player1.weaponList[player1.equippedWeapon]


pyglet.clock.schedule_interval(update, 1.0 / 120.0)
pyglet.app.run()