import pyglet
from pyglet.window import key

from resources import AGENT_IMAGES
from level import LEVEL_ROWS, LEVEL_COLUMNS, TILE_SIZE
from load import foreground

class Agent(pyglet.sprite.Sprite):
    '''Basic agent class. Anything that moves and reacts'''
    def __init__(self, x, y, level_layout, *args, **kwargs):
        super(Agent, self).__init__(x=x, y=y, group=foreground, *args, **kwargs)
        self.pos_x = x
        self.pos_y = y
        self.calculate_render_position()
        self.moves = 0
        self.level_layout = level_layout

    def calculate_render_position(self):
        self.x = self.pos_x* TILE_SIZE + TILE_SIZE/2.0
        self.y = self.pos_y*TILE_SIZE + TILE_SIZE/2.0

    def valid_move(self, direction):
        '''checks if the tile the agent is tryong to moving to is a valid tile'''
        to_x = self.pos_x
        to_y = self.pos_y
        if direction == 'right':
            to_x += 1
        elif direction == 'left':
            to_x -= 1
        elif direction == 'up':
            to_y += 1
        elif direction == 'down':
            to_y -= 1
        return self.level_layout[to_x, to_y] in ['floor','exit']

    def move_right(self):
        if self.pos_x < LEVEL_COLUMNS-1 and self.moves>0 and self.valid_move('right'):
            self.rotation = 270
            self.pos_x += 1
            self.moves -= 1

    def move_left(self):
        if self.pos_x > 0 and self.moves>0 and self.valid_move('left'):
            self.rotation = 90
            self.pos_x -= 1
            self.moves -= 1

    def move_up(self):
        if self.pos_y < LEVEL_ROWS-1 and self.moves>0 and self.valid_move('up'):
            self.pos_y += 1
            self.rotation = 180
            self.moves -= 1

    def move_down(self):
        if self.pos_y > 0 and self.moves>0 and self.valid_move('down'):
            self.pos_y -= 1
            self.rotation = 0
            self.moves -= 1

    def update(self, dt):
        self.calculate_render_position()

class Player(Agent):
    '''The player basic character'''
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=AGENT_IMAGES['player'], *args, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.moves = 100000

    def update(self, dt):
        if self.key_handler[key.LEFT]:
            self.move_left()
        elif self.key_handler[key.RIGHT]:
            self.move_right()
        elif self.key_handler[key.UP]:
            self.move_up()
        elif self.key_handler[key.DOWN]:
            self.move_down()
        super(Player, self).update(dt)
