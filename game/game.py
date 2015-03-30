from level import Level, level_layout
from agents import Player

class Game(object):
    '''main game class'''
    def __init__(self, batch):
        self.level = Level(level_layout, batch)
        player_x, player_y = self.level.find('entrance')
        self.agents = []
        player = Player(x=player_x, y=player_y, level_layout=self.level.layout, batch=batch)
        self.player = player
        self.agents.append(player)
