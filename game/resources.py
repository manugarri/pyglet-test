import pyglet

from load import foreground
from constants import TILE_SIZE


pyglet.resource.path = ['game/resources']
pyglet.resource.reindex()

i = pyglet.resource.image
anim = pyglet.resource.animation

TILE_IMAGES = {
 'wall': i('wall.png'),
 'floor': i('floor.png'),
 'entrance': i('entrance.png'),
 'exit': i('exit.png')
 }


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

AGENT_IMAGES = {
 'knight': i('knight.png'),
 'peasant': i('peasant.png'),
 'goblin': i('goblin.png'),
 'orc': i('orc.png'),
 'chest': i('chest.png')
}

map(center_image, AGENT_IMAGES.values())

FX = {
    'slice': i('slice.png')
}
map(center_image, FX.values())

def calculate_render_position(pos_x, pos_y):
    '''Converts from the tiles to screen pixels'''
    x = pos_x* TILE_SIZE + TILE_SIZE/2.0
    y = pos_y*TILE_SIZE + TILE_SIZE/2.0
    return x,y

class VisibleElement(pyglet.sprite.Sprite):
    #Basic agent class.
    def __init__(self, x, y, *args, **kwargs):
        super(VisibleElement, self).__init__(x=x, y=y, group=foreground, *args, **kwargs)
        self.pos_x = x
        self.pos_y = y
        self.calculate_render_position()

    def get_front_coords(self):
        '''utility that returns the coordinates in front of the agent'''
        to_x = self.pos_x
        to_y = self.pos_y
        if self.rotation == 270:
            to_x += 1
        elif self.rotation == 90:
            to_x -= 1
        elif self.rotation == 180:
            to_y += 1
        elif self.rotation == 0:
            to_y -= 1
        return to_x, to_y

    def calculate_render_position(self):
        '''Converts from the tiles to screen pixels'''
        self.x = self.pos_x* TILE_SIZE + TILE_SIZE/2.0
        self.y = self.pos_y*TILE_SIZE + TILE_SIZE/2.0

    def update(self, dt):
        self.calculate_render_position()
