import pyglet
from _boid import Boid

window = pyglet.window.Window()
# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=window.width//2,
#                           y=window.height//2,
#                           anchor_x='center',
#                           anchor_y='center')

boids = []
for i in range(10):
    boids.append(Boid())


def tick(time):
    for boid in boids:
        boid.tick()


@window.event
def on_draw():
    window.clear()
    for boid in boids:
        boid.draw()

pyglet.clock.schedule_interval(tick,1/60)
pyglet.app.run()