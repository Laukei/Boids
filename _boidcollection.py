from _boid import Boid

class BoidCollection:
    def __init__(self,*args,**kwargs):
        '''
        Collection of Boids.
        :param args:
        :param kwargs:
        '''
        self.boids = set()


    def add(self,number=None,**kwargs):
        if not number:
            number = 1
        for i in range(number):
            self.boids.add(Boid(**kwargs))


    def remove(self,boid):
        self.boids.remove(boid)


    def tick(self):
        for boid in self.boids:
            boid.tick()


    def draw(self):
        for boid in self.boids:
            boid.draw()