import pyglet

pyglet.resource.path = ['game/resources']
pyglet.resource.reindex()

i = pyglet.resource.image

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
 'chest': i('chest.png')
}

map(center_image, AGENT_IMAGES.values())
