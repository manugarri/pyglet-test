import pyglet

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

main_batch = pyglet.graphics.Batch()
level_batch = pyglet.graphics.Batch()
animation_batch = pyglet.graphics.Batch()

BATCHES = [
        level_batch,
        main_batch,
        animation_batch
        ]
