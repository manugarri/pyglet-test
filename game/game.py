import pyglet

from level import Level, GAME_WIDTH
from agents import Player

class Game(object):
    '''main game class'''
    def __init__(self, batch):
        self.level_number = 0
        self.level = Level(self.level_number, batch)
        self.batch = batch
        player_x, player_y = self.level.find('entrance')
        self.agents = []
        player = Player(x=player_x, y=player_y, level=self.level, batch=batch)
        self.player = player
        self.agents.append(player)
        self.label = pyglet.text.Label(text="Game started", x=GAME_WIDTH/2.0, y=5, anchor_x='center', batch=batch)
        self.notifications = []

    def load_level(self):
        self.level = Level(self.level_number, self.batch)
        self.player.pos_x, self.pos_y = self.level.find('entrance')
        self.agents = [self.player]
        self.notifications = []

    def update(self, dt):
        for agent in self.agents:
            agent.update(dt)
            self.notifications.extend(agent.notifications)
            agent.notifications = []
            self.display_notifications()

    def display_notifications(self):
        '''displays text'''
        for notification in self.notifications:
            self.label.text = notification
