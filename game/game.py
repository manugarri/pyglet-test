import pyglet

from level import Level
from constants import GAME_WIDTH
from agents import Player, AGENTS_CLASSES

class Game(object):
    '''main game class'''
    def __init__(self, main_batch, level_batch):
        self.level_number = 0
        self.level = Level(self.level_number, level_batch)
        self.batch = main_batch
        self.agents = self.level.load_agents(AGENTS_CLASSES, main_batch)
        self.register_dispatchers(self.agents)

        player_x, player_y = self.level.find('entrance')
        player = Player(x=player_x, y=player_y, level=self.level, batch=self.batch)
        self.player = player
        self.register_dispatchers(self.player._avatars)
        self.agents.append(player)

        self.label = pyglet.text.Label(text="Game started", x=GAME_WIDTH/2.0,
                y=5, anchor_x='center', batch=self.batch)

    def load_level(self):
        self.level = Level(self.level_number, self.batch)
        self.player.pos_x, self.pos_y = self.level.find('entrance')
        self.agents = [self.player]

    def register_dispatchers(self, agents):
        for agent in agents:
            agent.dispatcher.push_handlers(self)

    def update(self, dt):
        for agent in self.agents:
            agent.update(dt)

    def display_notifications(self, notifications):
        '''displays text'''
        for notification in notifications:
            self.label.text = notification
