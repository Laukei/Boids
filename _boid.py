import random
import math

import pyglet

DEFAULT_SIZE = 10
DEFAULT_SPEED = DEFAULT_SIZE/5
DEFAULT_VISION_RANGE = 50
DEFAULT_PALETTE = (180,180,255)
DEFAULT_BOUNDS = (0,640,0,480)
DEFAULT_TOLERANCE = 1E-8

def _randomise_palette(base):
    '''
    Selects approximately similar colours to given colour
    :param base: (r,g,b) tuple
    :return: [r,g,b] list of colours
    '''
    new_base = []
    for basecolour in base:
        interim_base = basecolour + random.randint(-40,40)
        interim_base = 0 if interim_base < 0 else 255 if interim_base > 255 else interim_base
        new_base.append(interim_base)
    return tuple(new_base)

def _random_position(bounds):
    '''
    Takes bounds and selects a random x,y coordinate within them
    :param bounds: (x1, x2, y1, y2) tuple of boundaries
    :return: position [x,y]
    '''
    x = random.randint(bounds[0],bounds[1])
    y = random.randint(bounds[2],bounds[3])
    return [x,y]


def _find_shortest_path(n1,n2,n_max,n_min=0):
    '''
    Finds the shortest distance between n1 and n2 including toroidal geometry
    :param n1: point 1
    :param n2: point 2
    :param n_max: maximum axis value
    :param n_min: minimum axis value
    :return: the signed displacement between n1 and n2
    '''
    width = n_max if n_min == 0 else n_max - n_min
    dn = n2 - n1
    dn = dn - width * round(dn/width)
    return dn


def get_displacement(boid_1,boid_2):
    '''
    returns absolute displacement between boid_1 and boid_2 including toroidal geometry
    :param boid_1: boid 1
    :param boid_2: boid 2
    :return: absolute displacement
    '''
    dx = _find_shortest_path(boid_1.position[0],boid_2.position[0],boid_1.bounds[1],boid_1.bounds[0])
    dy = _find_shortest_path(boid_1.position[1],boid_2.position[1],boid_1.bounds[3],boid_1.bounds[2])
    return (dx**2 + dy**2)**0.5


class Boid:
    def __init__(self, *args, **kwargs):
        '''
        Boid class. All parameters are passed as kwargs.

        :param kwargs:
        size: scaling factor for derived parameters of boid (width, length)
        width: sets width for boid (overrides size)
        length: sets length of boid (overrides size)
        palette: 3-part RGB tuple (0-255) for approximate colour of boid
        specific_colour:3-part RGB tuple for specific colour of boid
        orientation: angle (0-360) boid is travelling in
        speed: pixels-per-tick speed of boid
        bounds: area boids can move in
        position: (x,y) position
        vision_range: distance at which boid considers other boids
        collection: reference to container BoidCollection
        '''
        self.width = kwargs.get('width',kwargs.get('size',DEFAULT_SIZE))
        self.length = kwargs.get('length',kwargs.get('size',DEFAULT_SIZE*2))
        self.colour = kwargs.get('specific_colour',_randomise_palette(kwargs.get('palette',DEFAULT_PALETTE)))
        self.orientation = kwargs.get('orientation',random.randint(0,359))
        self.speed = kwargs.get('speed',DEFAULT_SPEED)
        self.bounds = kwargs.get('bounds',DEFAULT_BOUNDS)
        self.position = list(kwargs.get('position',_random_position(self.bounds)))
        self.vision_range = kwargs.get('vision_range',DEFAULT_VISION_RANGE)
        self.tolerance = kwargs.get('tolerance',DEFAULT_TOLERANCE)
        self.collection = kwargs.get('collection',None)

        self._last_orientation = None
        self._update_offsets()
        self.colour_info = tuple(self.colour*3)
        self._create_vertex_list()


    def tick(self):
        '''
        Increments one tick: update movement, perform move, check for boundary cross, update list of vertices for drawing
        '''
        self._get_recommendations()
        self._update_movement_vector()
        self.position[0] += self._movement_vector[0]
        self.position[1] += self._movement_vector[1]
        self._check_boundaries()
        self._update_vertex_list()


    def _get_recommendations(self):
        '''
        Performs 3 actions:
        1. gets recommendation for collision avoidance
        2. gets recommendation for velocity matching
        3. gets recommendation for flock centering
        then organises the recommendations and metes out suggested changes to boid
        '''
        self._get_recommendation_avoidance()
        self._get_recommendation_matching()
        self._get_recommendation_centering()


    def _get_recommendation_avoidance(self):
        pass


    def _get_recommendation_matching(self):
        pass


    def _get_recommendation_centering(self):
        pass


    def draw(self):
        '''
        Draws the Boid
        '''
        self.vertex_list.draw(pyglet.gl.GL_TRIANGLES)

    @property
    def angle(self):
        '''
        Calculates the angle in radians from the orientation
        :return: angle in radians
        '''
        if self._last_orientation != self.orientation:
            self._angle = math.pi * self.orientation / 180
        return self._angle


    def _create_vertex_list(self):
        '''
        Internal function, creates list of vertices for pyglet
        '''
        self.vertex_list = pyglet.graphics.vertex_list(
            3,
            ('v2f', self.get_vertices()),
            ('c3B', self.colour_info)
        )


    def _update_vertex_list(self):
        '''
        Internal function, updates vertex list position for pyglet
        '''
        self.vertex_list.vertices = self.get_vertices()


    def _update_offsets(self):
        '''
        Internal function, updates offsets tuple using length and width values
        '''
        self.offsets = ((self.length / 2, 0),
                        (-self.length / 2, -self.width / 2),
                        (-self.length / 2, self.width / 2))


    def get_vertices(self):
        '''
        Gets the vertices for use in vertex list
        :return (x1,y1,x2,y2,x3,y3): tuple of vertices
        '''
        self.vertices = []
        for x_offset, y_offset in self.offsets:
            self.vertices.append(self.position[0] + (x_offset * math.cos(self.angle) - (y_offset * math.sin(self.angle))))
            self.vertices.append(self.position[1] + (x_offset * math.sin(self.angle) + (y_offset * math.cos(self.angle))))
        return self.vertices


    def _check_boundaries(self):
        '''
        Internal function to update position if crossing a boundary (toroid boundary condition)
        '''
        if self.position[0] < (self.bounds[0] - self.tolerance):
            self.position[0] += self.bounds[1]
        elif self.position[0] > (self.bounds[1] + self.tolerance):
            self.position[0] -= self.bounds[1]
        if self.position[1] < (self.bounds[2] - self.tolerance):
            self.position[1] += self.bounds[3]
        elif self.position[1] > (self.bounds[3] + self.tolerance):
            self.position[1] -= self.bounds[3]


    def _update_movement_vector(self):
        '''
        Internal function to update the movement vector
        '''
        self._movement_vector = [self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)]