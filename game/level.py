'''
10x15 blocks
each block is 50x50 px

this means our game size is 500x750
'''
import pyglet
import numpy as np

from resources import TILE_IMAGES
from load import background

LEVEL_ROWS = 10
LEVEL_COLUMNS = 15
TILE_SIZE = 50 #50 by 50 px block


level_layout='''
#.#.#.#.#.#.#.#.#.#.#.#.#.#.#
#. . . . . . . . . . . . . .2
#. .#.#.#.#.#. . . . . . . .#
#. .#. . . . . . . . . . . .#
#. .#. . . . . . . . . . . .#
#.#.#. . . . . . . . . . . .#
#. . . . . . . . . . . . . .#
#. .#. . . . . . . . . . . .#
#. .#. . . . . . . . . . . .#
#.1.#.#.#.#.#.#.#.#.#.#.#.#.#
'''

level_objects='''
#.#.#.#.#.#.#.#.#.#.#.#.#.#.#
#. . . . . . . . . . . . . .2
#. .#.#.#.#.#. . . . . . .G.#
#. .#. . . . . . . . . . . .#
#.C.#. . . . . . . . . . . .#
#.#.#. . . . . . . . . . . .#
#. . . . . . . . . . . . .O.#
#. .#. . . . . . . . . . .O.#
#. .#. . . . . . . . . . . .#
#.1.#.#.#.#.#.#.#.#.#.#.#.#.#
'''
TEMPLATE_SYMBOLS = {
 '#': 'wall',
 ' ': 'floor',
 '1': 'entrance',
 '2': 'exit'
}

def parse_template(level_template):
    for key, value in TEMPLATE_SYMBOLS.items():
        level_template = level_template.replace(key, value)
    return level_template

class Level(object):
    '''the level object, it has many tiles'''
    def __init__(self, level_template, batch, *args, **kwargs):
        self.tiles = []
        self.layout = []
        self._layout = parse_template(level_template)
        self.read_template(batch)

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

class Tile(pyglet.sprite.Sprite):
    '''A Level tile has the sprite data'''
    def __init__(self, x, y, tile_type, batch, *args, **kwargs):
        self.tile_type = tile_type
        tile_image = TILE_IMAGES[tile_type]
        self.pos_x = x
        self.post_y = y
        x = x * TILE_SIZE
        y = y * TILE_SIZE
        super(Tile, self).__init__(tile_image, x=x, y=y, batch=batch, *args, **kwargs)
