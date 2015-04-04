import time

import pyglet

from level import Level
from constants import GAME_WIDTH, LEVEL_ROWS, LEVEL_COLUMNS
from agents import Player, AGENTS_CLASSES
from resources import VisibleElement, FX
from load import animation_batch

class Game(object):
    '''main game class'''
    def __init__(self, level_batch, main_batch, animation_batch):
        self.level_number = 0
        self.turn = 0
        self.turn_side = 'evil' #good guys start first
        self.animations = []
        self.level = Level(self.level_number, level_batch)
        self.batch = main_batch
        self.agents = self.level.load_agents(AGENTS_CLASSES, main_batch)
        player_x, player_y = self.level.find('entrance')
        player = Player(x=player_x, y=player_y, level=self.level, batch=self.batch)
        self.player = player

        self.register_dispatchers()
        self.label = pyglet.text.Label(text="Game started", x=GAME_WIDTH/2.0,
                y=5, anchor_x='center', batch=self.batch)
        self.reset_turn()

    def load_level(self):
        self.level = Level(self.level_number, self.batch)
        self.player.pos_x, self.pos_y = self.level.find('entrance')
        self.agents = [self.player]

    def register_dispatchers(self):
        for agent in self.agents:
            agent.dispatcher.push_handlers(self)
        for avatar in self.player._avatars:
            avatar.dispatcher.push_handlers(self)
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
        self.turn += 1
        if self.turn_side == 'evil':
            self.turn_side = 'good'
        else:
            self.turn_side = 'evil'
        self.display_notifications(['Turn of the {} guys'.format(self.turn_side)])
        for agent in self.agents + list(self.player._avatars):
            agent.reset_moves()

    def player_event(self, event_type):
        event_type = event_type[0]
        if event_type == 'end_turn':
            self.reset_turn()
