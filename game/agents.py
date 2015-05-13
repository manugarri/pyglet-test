import time
from collections import deque
from math import sqrt, pow

import pyglet
from pyglet.window import key

from resources import AGENT_IMAGES, VisibleElement
from constants import LEVEL_ROWS, LEVEL_COLUMNS

def agents_distance(x1,y1, x2, y2):
    '''returns the distance (in legal movements) between two elements in the level'''
    #return abs(x1-x2) + abs(y1-y2)
    return sqrt(pow(x1-x2,2)+pow(y1-y2,2))

class Agent(VisibleElement):
    #Basic Agent class
    def __init__(self, x, y, level, *args, **kwargs):
        super(Agent, self).__init__(x=x, y=y, *args, **kwargs)
        self.name = 'Stuff'
        self.side = 'neutral' #only 3 sides, good (avatars), bad (monsters) and neutral (chests)
        self.level = level
        self.dispatcher = pyglet.event.EventDispatcher()
        self.dispatcher.register_event_type('display_notifications')
        self.dispatcher.register_event_type('animation')
        self.level_info = {}
        self.health = 1

    def notify(self, message):
        #adds a text notification on the window
        self.dispatcher.dispatch_event('display_notifications', [message])

    def animation(self, animation_type, x, y):
        animation = {'name': animation_type,
                     'x': x,
                     'y': y
                     }
        self.dispatcher.dispatch_event('animation', [animation])

class ActiveAgent(Agent):
    def __init__(self, *args, **kwargs):
        #'''Agent that interacts'''
        super(ActiveAgent, self).__init__(*args, **kwargs)
        self.turn_moves = 0
        self.power = 0

    def reset_moves(self):
        self.moves = self.turn_moves

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
                self.level_info['agents'][to_x][to_y]==0:
            return True, to_x, to_y
        else:
            return False, to_x, to_y

    def move_right(self):
        self.rotation = 270
        if self.pos_x < LEVEL_COLUMNS-1 and self.moves>0 and self.valid_move('right')[0]:
            self.pos_x += 1
            self.moves -= 1
        else:
            return False

    def move_left(self):
        self.rotation = 90
        if self.pos_x > 0 and self.moves>0 and self.valid_move('left')[0]:
            self.pos_x -= 1
            self.moves -= 1
        else:
            return False

    def move_up(self):
        self.rotation = 180
        if self.pos_y < LEVEL_ROWS-1 and self.moves>0 and self.valid_move('up')[0]:
            self.pos_y += 1
            self.moves -= 1
        else:
            return False

    def move_down(self):
        self.rotation = 0
        if self.pos_y > 0 and self.moves>0 and self.valid_move('down')[0]:
            self.pos_y -= 1
            self.moves -= 1
        else:
            return False

    def check_position(self):
        pass

    def take_action(self):
        pass

    def attack(self):
        '''checks the tile in front of the agent. deducts the agent's power from the other's health
        only if both agents sides are different'''
        if self.moves <= 0:
            return False
        to_x, to_y = self.get_front_coords()
        attacked_agent = self.level_info['agents'][to_x][to_y]
        if attacked_agent !=0 and self.side != attacked_agent.side:
            attacked_agent.health -= self.power
            self.notify('{} attacks {}'.format(self.name, attacked_agent.name))
            self.animation('slice', to_x, to_y)
            self.moves -= 1
            return True
        return False

class BasicMob(ActiveAgent):
    '''basic mob with some logic to decide actions
    based on its a personality'''

    def __init__(self, *args, **kwargs):
        super(BasicMob, self).__init__(*args, **kwargs)
        self.personality_actions  ={
        'close_combat':[self.move_to_nearest_enemy,self.attack_enemy]}
        #'range_combat':[escape_if_too_close, get_shoot_range, shoot]
        self.personality = 'close_combat'
        self.side = 'evil' #good only attacks evil or neutral
        self.reset_moves()

    def take_action(self):
        '''decides what to do based on mob personality'''
        for step in self.personality_actions[self.personality]:
            step()

    def find_nearest_enemy(self):
        '''returns location of nearest enemy. If tie returns a random one'''
        enemies = [agent for agent in self.level_info['agents_list'] if agent.side != self.side and agent.side!='neutral']
        enemies_distances = [agents_distance(self.pos_x, self.pos_y,
                           enemy.pos_x, enemy.pos_y) for enemy in enemies]
        closest_distance = min(enemies_distances)
        return enemies[enemies_distances.index(closest_distance)], closest_distance

    def move_to_nearest_enemy(self):
        '''the mob moves to the nearest avatar.
        If there is one next to it, the mob attacks'''
        target, distance = self.find_nearest_enemy()
        print('{} moves ({} moves left) distance: {}'.format(self.name, self.moves - 1, distance))
        if distance <= 1:
            attacked = self.attack_enemy()
            if attacked:
                return None
        '''
        for direction in ['left','right','up','down']:
            valid_move, to_x, to_y = self.valid_move(direction)
            if valid_move and agents_distance(to_x, to_y, target.pos_x, target.pos_y) < \
                    agents_distance( self.pos_x, self.pos_y, target.pos_x, target.pos_y):
                eval('self.move_{}()'.format(direction))
                return None
        '''

        def get_movements():
            ''' for each direction, calculate the distance.
            for the minimum direction:
                return the direction name, the to_x and to_y
            '''
            directions = ['left','right','up','down']
            movements = []
            for direction in directions:
                valid_move, to_x, to_y = self.valid_move(direction)
                distance = agents_distance(to_x, to_y, target.pos_x, target.pos_y)
                movements.append([direction, distance, valid_move, to_x, to_y])
            movements = sorted(movements, key=lambda x: x[1])
            return movements

        movements = get_movements()
        for movement in movements:
            if movement[2] and movement[1]< distance:
                eval('self.move_{}()'.format(movement[0]))
                return None

        #should move tangential if no direct move is available
        if distance > 1:
            for movement in movements:
                if movement[2]:
                    eval('self.move_{}()'.format(movement[0]))
                    return None

        #change orientation when mob is next to avatar
        if target.pos_y > self.pos_y:
            self.move_up()
        elif target.pos_y < self.pos_y:
            self.move_down()
        elif target.pos_x > self.pos_x:
            self.move_right()
        else:
            self.move_left()

    def attack_enemy(self):
        '''attacks the enemy in range with the lowest health. Random if tie'''
        target,distance = self.find_nearest_enemy()
        if distance <= 1:
            attacked = self.attack()
            if attacked:
                return True
        return False

    def escape_if_too_close(self):
        '''the mob escapes if its within 3 movement blocks it will move on the
        opposite direction'''

    '''
    def update(self, dt):
        self.decide_action()
        super(BasicMob, self).update(dt)
    '''
class Player(object):
    '''The player basic character'''
    def __init__(self, avatars, *args, **kwargs):
        self.key_handler = key.KeyStateHandler()
        self.load_avatars(avatars, *args, **kwargs)
        self.dispatcher = pyglet.event.EventDispatcher()
        self.dispatcher.register_event_type('player_event')

    def load_avatars(self, avatars, *args, **kwargs):

        try:
            if hasattr(self,'_avatars'):
                for old_avatar in self._avatars:
                    old_avatar.delete()
        except Exception as e:
            print(e)

        self._avatars = [AVATARS_CLASSES[avatar](*args, **kwargs) for avatar in avatars]
        self._avatars = deque(self._avatars)
        self.avatar = self._avatars[0]

    def sleep(self):
        time.sleep(0.1)
        pass

    def update(self, turn_side, dt):
        if turn_side != 'good':
            return None
        if self.key_handler[key.LEFT]:
            self.avatar.move_left()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
        elif self.key_handler[key.RIGHT]:
            self.avatar.move_right()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
        elif self.key_handler[key.UP]:
            self.avatar.move_up()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
        elif self.key_handler[key.DOWN]:
            self.avatar.move_down()
            self.avatar.notify('{} moves left {}'.format(self.avatar.name, self.avatar.moves))
        elif self.key_handler[key.SPACE]:
            self.change_avatar()
            self.avatar.notify('{} Selected'.format(self.avatar.name))
        elif self.key_handler[key.A]:
            self.avatar.attack()
        elif self.key_handler[key.ENTER]:
            print('\nkey enter pressed\n')
            self.sleep()
            self.dispatcher.dispatch_event('player_event', ['end_turn'])
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
        self.side = 'good' #good only attacks evil or neutral
        self.turn_moves = 4
        self.health = 3
        self.power = 1
        self.reset_moves()

class Knight(ActiveAgent):
    '''The knight has a good health/power ratio'''
    def __init__(self, *args, **kwargs):
        super(Knight, self).__init__(img=AGENT_IMAGES['knight'], *args, **kwargs)
        self.name = 'Knight'
        self.side = 'good' #good only attacks evil or neutral
        self.turn_moves = 3
        self.health = 5
        self.power = 2
        self.reset_moves()

class Goblin(BasicMob):
    '''Weakest of all mobs.'''
    def __init__(self, *args, **kwargs):
        super(Goblin, self).__init__(img=AGENT_IMAGES['goblin'], *args, **kwargs)
        self.name = 'Goblin'
        self.health = 3
        self.turn_moves = 3
        self.power = 1

class Chest(ActiveAgent):
    '''A chest'''
    def __init__(self, *args, **kwargs):
        super(Chest, self).__init__(img=AGENT_IMAGES['chest'], *args, **kwargs)
        self.name = 'Chest'
        self.moves = 0

AGENTS_CLASSES = {
'chest': Chest,
'goblin': Goblin
    }

AVATARS_CLASSES = {
'peasant': Peasant,
'knight': Knight
}
