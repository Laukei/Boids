import pyglet
from _boidcollection import BoidCollection


def main():
    window = pyglet.window.Window()
    boids = BoidCollection()
    boids.add(40)
    # boids.add(id=0,position=(11,10),orientation=0)#,bounds=(0,200,0,200))
    # boids.add(id=90,position=(10,11),orientation=0)#,bounds=(0,200,0,200))
    # boids.add(id=-215,position=(1,1),orientation=0)#,bounds=(0,200,0,200))
    # boids.add(position=(300,300),orientation=90)
    # boids.add(position=(310,330),orientation=90)


    def tick(time):
        boids.tick()


    @window.event
    def on_draw():
        window.clear()
        boids.draw()

    pyglet.clock.schedule_interval(tick,1/60)
    pyglet.app.run()


if __name__ == "__main__":
    main()