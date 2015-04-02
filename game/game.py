import pyglet

from level import Level
from constants import GAME_WIDTH, LEVEL_ROWS, LEVEL_COLUMNS
from agents import Player, AGENTS_CLASSES
import numpy  as np


class Game(object):
    '''main game class'''
    def __init__(self, main_batch, level_batch):
        self.level_number = 0
        self.level = Level(self.level_number, level_batch)
        self.batch = main_batch
        self.agents = self.level.load_agents(AGENTS_CLASSES, main_batch)

        player_x, player_y = self.level.find('entrance')
        player = Player(x=player_x, y=player_y, level=self.level, batch=self.batch)
        self.player = player

        self.register_dispatchers()
        self.label = pyglet.text.Label(text="Game started", x=GAME_WIDTH/2.0,
                y=5, anchor_x='center', batch=self.batch)

    def load_level(self):
        self.level = Level(self.level_number, self.batch)
        self.player.pos_x, self.pos_y = self.level.find('entrance')
        self.agents = [self.player]

    def register_dispatchers(self):
        for agent in self.agents:
            agent.dispatcher.push_handlers(self)
        for avatar in self.player._avatars:
            avatar.dispatcher.push_handlers(self)

    def update(self, dt):
        for agent in self.agents:
            agent.update(dt)
        self.player.update(dt)
        self.update_agents_level_info()

    def update_agents_level_info(self):
        '''updates agents knowledge of other level agents, events,etc'''
        level_info = {}
        level_info['agents'] = np.zeros(shape=(LEVEL_COLUMNS, LEVEL_ROWS)).tolist()
        level_info['avatars'] = np.zeros(shape=(LEVEL_COLUMNS, LEVEL_ROWS)).tolist()
        for agent in self.agents:
           level_info['agents'][agent.pos_x][agent.pos_y] = {
                'name': agent.name,
                'pos_x': agent.pos_x,
                'pos_y': agent.pos_y
                }
        for avatar in self.player._avatars:
           level_info['avatars'][avatar.pos_x][avatar.pos_y] = {
                'name': avatar.name,
                'pos_x': avatar.pos_x,
                'pos_y': avatar.pos_y
                }
        for agent in self.agents + list(self.player._avatars):
            agent.level_info = level_info

    def display_notifications(self, notifications):
        '''displays text'''
        for notification in notifications:
            self.label.text = notification
