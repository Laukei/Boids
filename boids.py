import pyglet
from _boid import Boid, BoidCollection


def main():
    window = pyglet.window.Window()
    boids = BoidCollection()
    boids.add(60)


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