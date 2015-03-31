import time
from collections import deque

import pyglet
from pyglet.window import key

from resources import AGENT_IMAGES
from level import LEVEL_ROWS, LEVEL_COLUMNS, TILE_SIZE
from load import foreground

class Agent(pyglet.sprite.Sprite):
    '''Basic agent class. Anything that moves and reacts'''
    def __init__(self, x, y, level, *args, **kwargs):
        super(Agent, self).__init__(x=x, y=y, group=foreground, *args, **kwargs)
        self.pos_x = x
        self.pos_y = y
        self.calculate_render_position()
        self.initial_moves = 5
        self.moves = 5
        self.level = level
        self.notifications = []

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
        return self.level.tiles[to_x, to_y].tile_type in ['floor','exit']

    def move_right(self):
        self.rotation = 270
        if self.pos_x < LEVEL_COLUMNS-1 and self.moves>0 and self.valid_move('right'):
            self.pos_x += 1
            self.moves -= 1

    def move_left(self):
        self.rotation = 90
        if self.pos_x > 0 and self.moves>0 and self.valid_move('left'):
            self.pos_x -= 1
            self.moves -= 1

    def move_up(self):
        self.rotation = 180
        if self.pos_y < LEVEL_ROWS-1 and self.moves>0 and self.valid_move('up'):
            self.pos_y += 1
            self.moves -= 1

    def move_down(self):
        self.rotation = 0
        if self.pos_y > 0 and self.moves>0 and self.valid_move('down'):
            self.pos_y -= 1
            self.moves -= 1

    def check_position(self):
        pass

    def update(self, dt):
        self.calculate_render_position()
        self.check_position()

class Player(object):
    '''The player basic character'''
    def __init__(self, *args, **kwargs):
        self.key_handler = key.KeyStateHandler()
        self._avatars = deque([
            Peasant(*args, **kwargs),
            Knight(*args, **kwargs)
        ])
        self.avatar = self._avatars[0]
        self.notifications = []

    def sleep(self):
        time.sleep(0.2)

    def update(self, dt):
        if self.key_handler[key.LEFT]:
            self.avatar.move_left()
            self.notifications.append('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.RIGHT]:
            self.avatar.move_right()
            self.notifications.append('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.UP]:
            self.avatar.move_up()
            self.notifications.append('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.DOWN]:
            self.avatar.move_down()
            self.notifications.append('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.SPACE]:
            self.change_avatar()
            self.notifications.append('{} Selected'.format(self.avatar.name))
            self.sleep()
        self.avatar.update(dt)
        self.check_position()

    def check_position(self):
        self.check_exit()

    def check_exit(self):
        '''checks if the player is in the exit'''

    def change_avatar(self):
        '''cycle avatar'''
        self._avatars.rotate()
        self.avatar = self._avatars[0]

class Peasant(Agent):
    '''Basic player avatar'''
    def __init__(self, *args, **kwargs):
        super(Peasant, self).__init__(img=AGENT_IMAGES['peasant'], *args, **kwargs)
        self.name = 'Peasant'

class Knight(Agent):
    '''The knight has a good health/power ratio'''
    def __init__(self, *args, **kwargs):
        super(Knight, self).__init__(img=AGENT_IMAGES['knight'], *args, **kwargs)
        self.name = 'Knight'

class Orc(Agent):
    '''The knight has a good health/power ratio'''
    def __init__(self, *args, **kwargs):
        super(Knight, self).__init__(img=AGENT_IMAGES['orc'], *args, **kwargs)
        self.name = 'Orc'
