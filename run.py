import pyglet

from game.level import LEVEL_ROWS, LEVEL_COLUMNS, TILE_SIZE
from game.game import Game

import logging
logging.basicConfig(level=logging.DEBUG)

GAME_HEIGHT = LEVEL_ROWS * TILE_SIZE
GAME_WIDTH = LEVEL_COLUMNS * TILE_SIZE

game_window = pyglet.window.Window(GAME_WIDTH, GAME_HEIGHT)
main_batch = pyglet.graphics.Batch()
game = Game(main_batch)
game_window.push_handlers(game.player)
game_window.push_handlers(game.player.key_handler)
#game_window.push_handlers(pyglet.window.event.WindowEventLogger())
#import ipdb; ipdb.set_trace()

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

def update(dt):
    for obj in game.agents:
        obj.update(dt)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/10.0)#/60.0)
    pyglet.app.run()
