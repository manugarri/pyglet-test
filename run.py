import pyglet

from game.level import GAME_WIDTH, GAME_HEIGHT
from game.game import Game


game_window = pyglet.window.Window(GAME_WIDTH, GAME_HEIGHT)
main_batch = pyglet.graphics.Batch()
game = Game(main_batch)
game_window.push_handlers(game.player.key_handler)
#game_window.push_handlers(pyglet.window.event.WindowEventLogger())
#import ipdb; ipdb.set_trace()

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(game.update, 1/60.0)#/60.0)
    pyglet.app.run()
