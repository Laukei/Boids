from _boid import Boid, get_displacement


class BoidCollection:
    def __init__(self,*args,**kwargs):
        '''
        Collection of Boids.
        :param args:
        :param kwargs:
        '''
        self.boids = set()
        self._init_displacements()


    def _init_displacements(self):
        '''
        Creates blank displacements container
        '''
        self.displacements = {boid:{} for boid in self.boids}
        self.displacements_up_to_date = False


    def add(self,number=None,**kwargs):
        '''
        add(): Adds a boid, passing kwargs to boid constructor
        add(number): Adds number of boids, passing kwargs to boid constructor
        :returns: list of boids created
        '''
        if not kwargs.get('collection'):
            kwargs['collection'] = self
        if not number:
            number = 1
        newboids = []
        for i in range(number):
            b = Boid(**kwargs)
            self.boids.add(b)
            newboids.append(b)
        self._init_displacements()
        return newboids


    def remove(self,boid):
        '''
        Removes boid from collection
        '''
        self.boids.remove(boid)
        self._init_displacements()


    def _update_displacements(self):
        '''
        Updates displacements between boids (only needs calling if displacements are not up to date)
        '''
        for boid_1 in self.boids:
            for boid_2 in self.boids:
                if boid_1 != boid_2:
                    self.displacements[boid_1][boid_2] = get_displacement(boid_1,boid_2)
        self.displacements_up_to_date = True


    def get_displacements(self):
        if not self.displacements_up_to_date:
            self._update_displacements()
        return self.displacements


    def tick(self):
        '''
        Ticks every boid
        '''
        for boid in self.boids:
            boid.decide_movement_strategy()
        for boid in self.boids:
            boid.tick()
        self.displacements_up_to_date = False


    def draw(self):
        '''
        Draws every boid
        '''
        for boid in self.boids:
            boid.draw()