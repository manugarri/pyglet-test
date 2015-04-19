import pyglet

from game.constants import GAME_WIDTH, GAME_HEIGHT
from game.game import Game
from game.load import BATCHES

game_window = pyglet.window.Window(GAME_WIDTH, GAME_HEIGHT)
main_batch = pyglet.graphics.Batch()
level_batch = pyglet.graphics.Batch()
game = Game(*BATCHES)
game_window.push_handlers(game.player.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    for batch in BATCHES:
        batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(game.update, 1/60.0)
    pyglet.app.run()
