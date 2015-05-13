import time

import pyglet

from level import Level
from constants import GAME_WIDTH, LEVEL_ROWS, LEVEL_COLUMNS
from agents import Player, AGENTS_CLASSES
from resources import VisibleElement, FX
from load import level_batch, animation_batch, main_batch

class Game(object):
    '''main game class'''
    def __init__(self, level_batch, main_batch, animation_batch):
        self.level_number = 0
        self.batch = main_batch
        self.label = pyglet.text.Label(text="Game started", x=GAME_WIDTH/2.0,
                y=5, anchor_x='center', batch=main_batch)
        self.load_level()

    def load_level(self):
        print('\n\n****************\nLOAD LEVEL********\n')
        self.turn = 0
        self.turn_side = 'evil' #good guys start first
        self.animations = []
        self.level = Level(self.level_number, level_batch)
        self.agents = self.level.load_agents(AGENTS_CLASSES, main_batch)
        self.load_player()
        self.register_dispatchers()
        self.level_number +=1
        self.reset_turn()

    def check_moves(self):
        for agent in self.agents:
            print('{} MOVES: {}'.format(agent.name, agent.moves))
        for avatar in self.player._avatars:
            print('{} MOVES: {}'.format(avatar.name, avatar.moves))

    def load_player(self):
        '''Creates the player or if already exists,reset the avatars location'''
        player_x, player_y = self.level.find('entrance')
        if hasattr(self,'player'):
            self.player.load_avatars(avatars=self.level.avatars, x=player_x, y=player_y, level=self.level, batch=main_batch)
            '''
            for avatar in self.player._avatars:
                avatar.pos_x = player_x
                avatar.pos_y = player_y
                avatar.level = self.level
                '''
        else:
            player = Player(avatars=self.level.avatars, x=player_x, y=player_y, level=self.level, batch=main_batch)
            self.player = player

    def register_dispatchers(self):
        for agent in self.agents:
            agent.dispatcher.push_handlers(self)
        for avatar in self.player._avatars:
            avatar.dispatcher.push_handlers(self)
        self.player.dispatcher.remove_handlers(self)
        self.player.dispatcher.push_handlers(self)

    def remove_dead(self, group):
        '''remove those agents with health 0'''
        for i, agent in enumerate(self.agents):
            if agent.health<=0:
                self.display_notifications(['{} was killed'.format(agent.name)])
                agent.delete()
                self.agents.pop(i)

    def update(self, dt):
        if self.turn_side == 'good':
            time.sleep(0.15)
        else:
            time.sleep(0.2)
        for animation in self.animations:
            try:
                animation.delete()
            except AttributeError:
                del animation

        self.remove_dead(self.agents)
        self.remove_dead(self.player._avatars)
        self.player.update(self.turn_side, dt)
        for agent in self.agents:
            if self.turn_side == agent.side:
                agent.take_action()
            agent.update(dt)
        if self.turn_side == 'evil':
            if sum([agent.moves for agent in self.agents])<=0:
                self.reset_turn()

        self.update_agents_level_info()
        self.check_victory()

    def update_agents_level_info(self):
        '''updates agents knowledge of other level agents, events,etc'''
        level_info = {}
        level_info['agents'] = [[0 for r in range(LEVEL_ROWS)] for c in range(LEVEL_COLUMNS)]
        level_info['agents_list'] = []
        for agent in self.agents:
           level_info['agents'][agent.pos_x][agent.pos_y] = agent
           level_info['agents_list'].append(agent)
        for avatar in self.player._avatars:
            level_info['agents'][avatar.pos_x][avatar.pos_y] = avatar
            level_info['agents_list'].append(avatar)
        for agent in self.agents + list(self.player._avatars):
            agent.level_info = level_info

    def display_notifications(self, notifications):
        '''displays text'''
        for notification in notifications:
            self.label.text = notification

    def animation(self, animations):
        animation = animations[0]
        animation = VisibleElement(img=FX[animation['name']], x=animation['x'],
                                   y=animation['y'], batch=animation_batch)
        self.animations.append(animation)

    def reset_turn(self):
        print('\n\n****************\nRESET TURN********')

        self.turn += 1
        if self.turn_side == 'evil':
            self.turn_side = 'good'
        else:
            self.turn_side = 'evil'
        print('\nTURN {} {}\n'.format(self.turn, self.turn_side))
        self.display_notifications(['Turn of the {} guys'.format(self.turn_side)])
        for agent in self.agents + list(self.player._avatars):
            agent.reset_moves()

    def player_event(self, event_type):
        print('\nplayer event: {}\n'.format(event_type[0]))
        event_type = event_type[0]
        if event_type == 'end_turn':
            self.reset_turn()

    def check_victory(self):
        if self.victory_condition():
            print('victory')
            self.display_notifications(['You win!'])
            time.sleep(0.5)
            self.load_level()

    def victory_condition(self):
        for condition in self.level.victory_conditions:
            if condition == 'kill':
                return len([agent for agent in self.agents if agent.side == 'evil'])<=0
            elif condition == 'exit':
                return len([a for a in self.player._avatars if
                            self.level.tiles[a.pos_x][a.pox_y].tile_type =='exit'])>=0
