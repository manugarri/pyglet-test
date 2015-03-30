import pyglet

pyglet.resource.path = ['game/resources']
pyglet.resource.reindex()
#TEXTURE_PATH = 'tiles.png'
# A TextureGroup manages an OpenGL texture.
#tile_texture = TextureGroup(image.load(TEXTURE_PATH).get_texture())

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
 'player': i('player.png')
}

map(center_image, AGENT_IMAGES.values())
