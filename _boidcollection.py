from _boid import Boid


def _find_shortest_path(n1,n2,n_max,n_min=0):
    width = n_max if n_min == 0 else n_max - n_min
    dn = n2 - n1
    dn = dn - width * round(dn/width)
    return abs(dn)


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
        if not kwargs.get('collection'):
            kwargs['collection'] = self
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