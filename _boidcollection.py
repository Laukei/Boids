from _boid import Boid

class BoidCollection:
    def __init__(self,*args,**kwargs):
        '''
        Collection of Boids.
        :param args:
        :param kwargs:
        '''
        self.boids = set()
        self.displacements_up_to_date = False


    def add(self,number=None,**kwargs):
        '''
        add(): Adds a boid, passing kwargs to boid constructor
        add(number): Adds number of boids, passing kwargs to boid constructor
        '''
        if not number:
            number = 1
        for i in range(number):
            self.boids.add(Boid(**kwargs))


    def remove(self,boid):
        '''
        Removes boid from collection
        '''
        self.boids.remove(boid)


    def _update_displacements(self):
        '''
        Updates displacements between boids (only needs calling if displacements are not up to date)
        '''
        #
        # do the actual work here
        #
        self.displacements_up_to_date = True


    def tick(self):
        '''
        Ticks every boid
        '''
        for boid in self.boids:
            boid.tick()
        self.displacements_up_to_date = False


    def draw(self):
        '''
        Draws every boid
        '''
        for boid in self.boids:
            boid.draw()