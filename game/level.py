'''
10x15 blocks
each block is 50x50 px

this means our game size is 500x750
'''
import pyglet
import numpy as np

from resources import TILE_IMAGES
from load import background
from level_templates import templates, TEMPLATE_SYMBOLS, AGENT_SYMBOLS
from constants import TILE_SIZE

def parse_template(level_template, symbols_map=TEMPLATE_SYMBOLS):
    for key, value in TEMPLATE_SYMBOLS.items():
        level_template = level_template.replace(key, value)
    return level_template

class Level(object):
    '''the level object, it has many tiles'''
    def __init__(self, number, batch, *args, **kwargs):
        self.number = number
        self.load_template()
        self.tiles = []
        self.layout = []
        self.read_template(batch)

    def load_template(self):
        template = templates['level_{}'.format(self.number)]
        self.victory_conditions = template['victory_conditions']
        self._layout = parse_template(template['layout'])
        self._agent_layout = parse_template(template['agents'], symbols_map=AGENT_SYMBOLS)

    def read_template(self, batch):
        '''Parses the template'''
        #pyglet x,y is bottom left and template is top left, so we reverse the rows
        for row, template_row in enumerate(reversed(self._layout.split('\n')[1:-1])):
            self.tiles.append([])
            self.layout.append([])
            for col, tile_type in enumerate(template_row.split('.')):
                tile_x = col
                tile_y = row
                self.layout[row].append(tile_type)
                self.tiles[row].append(Tile(tile_x, tile_y, tile_type, batch))
        self.tiles = np.transpose(np.array(self.tiles))
        self.layout = np.transpose(np.array(self.layout))

    def find(self, element):
        '''returns first instance where an element exists in a layout'''
        return np.where(self.layout==element)[0][0], np.where(self.layout==element)[1][0]

    def get_tile_type(self, x, y):
        '''returns the level tile_type of the pos x,y'''
        return self.layout[x, y]

    def load_agents(self):
        agent_symbols = AGENT_SYMBOLS.keys()
        return []


class Tile(pyglet.sprite.Sprite):
    '''A Level tile has the sprite data'''
    def __init__(self, x, y, tile_type, batch, group=background, *args, **kwargs):
        self.tile_type = tile_type
        tile_image = TILE_IMAGES[tile_type]
        self.pos_x = x
        self.post_y = y
        x = x * TILE_SIZE
        y = y * TILE_SIZE
        super(Tile, self).__init__(tile_image, x=x, y=y, batch=batch, *args, **kwargs)
