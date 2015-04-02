import time
from collections import deque

import pyglet
from pyglet.window import key

from resources import AGENT_IMAGES
from constants import LEVEL_ROWS, LEVEL_COLUMNS, TILE_SIZE
from load import foreground

class Agent(pyglet.sprite.Sprite):
    #Basic agent class. Anything that interacts
    def __init__(self, x, y, level, *args, **kwargs):
        super(Agent, self).__init__(x=x, y=y, group=foreground, *args, **kwargs)
        self.name = 'Stuff'
        self.side = 'neutral' #only 3 sides, good (avatars), bad (monsters) and neutral (chests)
        self.pos_x = x
        self.pos_y = y
        self.calculate_render_position()
        self.level = level
        self.dispatcher = pyglet.event.EventDispatcher()
        self.dispatcher.register_event_type('display_notifications')
        self.level_info = []
        self.health = 1

    def notify(self, message):
        '''adds a text notification on the window'''
        self.dispatcher.dispatch_event('display_notifications', [message])

    def calculate_render_position(self):
        '''Converts from the tiles to screen pixels'''
        self.x = self.pos_x* TILE_SIZE + TILE_SIZE/2.0
        self.y = self.pos_y*TILE_SIZE + TILE_SIZE/2.0

    def update(self, dt):
        self.calculate_render_position()

class ActiveAgent(Agent):
    def __init__(self, *args, **kwargs):
        '''Agent that moves, thinks and attacks'''
        super(ActiveAgent, self).__init__(*args, **kwargs)
        self.initial_moves = 5
        self.moves = 5

    def valid_move(self, direction):
        #checks if the tile the agent is tryong to moving to is a valid tile
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
        if self.level.tiles[to_x, to_y].tile_type in ['floor','exit'] and\
                self.level_info['agents'][to_x][to_y]==0 and\
                self.level_info['avatars'][to_x][to_y]==0:
            return True
        else:
            return False

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

class Player(object):
    '''The player basic character'''
    def __init__(self, *args, **kwargs):
        self.key_handler = key.KeyStateHandler()
        self._avatars = deque([
            Peasant(*args, **kwargs),
            Knight(*args, **kwargs)
        ])
        self.avatar = self._avatars[0]

    def sleep(self):
        time.sleep(0.2)

    def update(self, dt):
        if self.key_handler[key.LEFT]:
            self.avatar.move_left()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.RIGHT]:
            self.avatar.move_right()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.UP]:
            self.avatar.move_up()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.DOWN]:
            self.avatar.move_down()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
            self.sleep()
        elif self.key_handler[key.SPACE]:
            self.change_avatar()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
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

class Peasant(ActiveAgent):
    '''Basic player avatar'''
    def __init__(self, *args, **kwargs):
        super(Peasant, self).__init__(img=AGENT_IMAGES['peasant'], *args, **kwargs)
        self.name = 'Peasant'
        self.moves = 100
        self.health = 3
        self.side = 'good' #good only attacks evil or neutral

class Knight(ActiveAgent):
    '''The knight has a good health/power ratio'''
    def __init__(self, *args, **kwargs):
        super(Knight, self).__init__(img=AGENT_IMAGES['knight'], *args, **kwargs)
        self.name = 'Knight'
        self.moves = 1000
        self.side = 'good' #good only attacks evil or neutral
        self.health = 5

class Goblin(ActiveAgent):
    '''Weakest of all mobs.'''
    def __init__(self, *args, **kwargs):
        super(Goblin, self).__init__(img=AGENT_IMAGES['goblin'], *args, **kwargs)
        self.name = 'Goblin'
        self.side = 'evil' #good only attacks evil or neutral

class Chest(Agent):
    '''A chest'''
    def __init__(self, *args, **kwargs):
        super(Chest, self).__init__(img=AGENT_IMAGES['chest'], *args, **kwargs)
        self.name = 'Chest'

AGENTS_CLASSES = {
'chest': Chest,
'goblin': Goblin
    }
