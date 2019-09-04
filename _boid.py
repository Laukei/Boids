import random
import math

import pyglet
from shapely.geometry import LineString, Point

from _boidlogic import Priority, sign

DEFAULT_SIZE = 10
DEFAULT_SPEED = DEFAULT_SIZE/5
DEFAULT_VISION_RANGE = 60
DEFAULT_PALETTE = (180,180,255)
DEFAULT_BOUNDS = (0,640,0,480)
DEFAULT_TOLERANCE = 1E-8
DEFAULT_VISION_ANGLE = 135

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
    x = _find_shortest_path(boid_1.position[0],boid_2.position[0],boid_1.bounds[1],boid_1.bounds[0])
    y = _find_shortest_path(boid_1.position[1],boid_2.position[1],boid_1.bounds[3],boid_1.bounds[2])
    return distance_between_points((0,0),(x,y))


def distance_between_points(p1,p2):
    '''
    returns distance between (x1,y1) and (x2,y2)
    :param p1: (x1,y1)
    :param p2: (x2,y2)
    :return: cartesian distance between points
    '''
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return (dx**2 + dy**2)**0.5


def adjust_position_for_boundaries(position,bounds,tolerance=DEFAULT_TOLERANCE):
    '''
    Function to update position if crossing a boundary (toroid boundary condition)
    :param position: (x,y) position
    :param bounds: (xmin,xmax,ymin,ymax) boundaries
    :param tolerance: optional tolerance for being on boundary (for rounding errors), DEFAULT_TOLERANCE
    '''
    position = list(position[:])
    if position[0] < (bounds[0] - tolerance):
        position[0] += bounds[1]
    elif position[0] > (bounds[1] + tolerance):
        position[0] -= bounds[1]
    if position[1] < (bounds[2] - tolerance):
        position[1] += bounds[3]
    elif position[1] > (bounds[3] + tolerance):
        position[1] -= bounds[3]
    return position


def check_for_collision(boid_1,boid_2):
    '''
    Determines if collision will happen
    :param boid_1
    :param boid_2
    :return:
    '''
    boid_1_position = boid_1.position
    boid_2_position = (boid_1.position[0] + _find_shortest_path(boid_1.position[0],boid_2.position[0],boid_1.bounds[1],boid_1.bounds[0]),
                       boid_2.position[1] + _find_shortest_path(boid_1.position[1],boid_2.position[1],boid_1.bounds[3],boid_1.bounds[2]))
    boid_1_heading = boid_1.get_heading(False)
    boid_2_heading = boid_2.get_heading(False)
    boid_2_heading = (boid_1.position[0] + _find_shortest_path(boid_1.position[0],boid_2_heading[0],boid_1.bounds[1],boid_1.bounds[0]),
                       boid_2.position[1] + _find_shortest_path(boid_1.position[1],boid_2_heading[1],boid_1.bounds[3],boid_1.bounds[2]))
    l1 = LineString((boid_1_position,boid_1_heading))
    l2 = LineString((boid_2_position,boid_2_heading))
    #print(boid_1.position,boid_1.get_heading(),l1,boid_2.position,boid_2.get_heading(),l2)
    if l1.intersects(l2):
        # if these intersect, check angle between vectors:
        # boid_1_angle = (180 * math.atan((boid_1_heading[1]-boid_1_position[1])/(boid_1_heading[0]-boid_1_heading[0]))/math.pi)%360
        # boid_2_angle = (180 * math.atan((boid_2_heading[1]-boid_2_position[1])/(boid_2_heading[0]-boid_2_heading[0]))/math.pi)%360
        recommended_orientation_change = -1 if (boid_2.orientation - boid_1.orientation)%180 > 90 else 1
        recommendation_severity = 1/(Point((boid_1_position)).distance(l1.intersection(l2))+0.0001)
        return (recommendation_severity,recommended_orientation_change)
    else:
        return (0,0)


def angle_between_vectors(v1, v2):
    '''
    Returns absolute angle between two vectors
    :param v1: vector 1
    :param v2: vector 2
    :return: theta in degrees
    '''
    numerator = ((v2[0] * v1[0]) + (v2[1] * v1[1]))
    denominator = ((v2[0] ** 2 + v2[1] ** 2) ** 0.5) * (
            ((v1[0] ** 2) + (v1[1] ** 2)) ** 0.5)
    opp_over_adj = sign(numerator) * float('inf') if denominator == 0 else numerator / denominator
    theta = math.acos(opp_over_adj) * 180 / math.pi
    return theta


class Boid:
    def __init__(self, *args, **kwargs):
        '''
        Boid class. All parameters are passed as kwargs.

        :param kwargs:
        id: optical name for identifying boid
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
        vision_angle: angle to which Boid can see neighbours
        '''
        self.id = kwargs.get('id',None)
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
        self.vision_angle = kwargs.get('vision_angle',DEFAULT_VISION_ANGLE)

        self.logic = Priority(self.speed)

        self._last_orientation = None
        self._update_offsets()
        self.colour_info = tuple(self.colour*3)
        self._create_vertex_list()
        self._new_position()


    def decide_movement_strategy(self):
        '''
        Look around boid to decide how to move when tick() called
        '''
        self._get_recommendations()


    def tick(self):
        '''
        Increments one tick: update movement, perform move, check for boundary cross, update list of vertices for drawing
        '''
        self._update_movement_vector()
        self.position[0] += self._movement_vector[0]
        self.position[1] += self._movement_vector[1]
        self._check_boundaries()
        self._update_vertex_list()
        self._new_position()


    def _get_recommendations(self):
        '''
        Performs 3 actions:
        1. gets recommendation for collision avoidance
        2. gets recommendation for velocity matching
        3. gets recommendation for flock centering
        then organises the recommendations and metes out suggested changes to boid
        '''
        recommendations = [self._get_recommendation_avoidance(),
                           self._get_recommendation_matching(),
                           self._get_recommendation_centering()]
        change = self.logic.from_recommendations(recommendations)
        self.orientation += change
        self.orientation = self.orientation % 360


    def _get_recommendation_avoidance(self):
        '''
        1. determines any collisions within sight range
        2. prioritise which is most important to avoid
        3. make recommendation and severity
        :return: recommendation (severity,change_direction)
        '''
        recommendation = (0,0)
        if self.neighbours:
            for neighbour in self.neighbours:
                n_recommend = check_for_collision(self,neighbour)
                if n_recommend[1] > recommendation[1]:
                    recommendation = n_recommend
        return recommendation


    def _get_recommendation_matching(self):
        '''
        Finds neighbours, looks at average difference in orientation, suggests a change to orientation to minimize this
        :return: recommended orientation change
        '''
        average_delta_orientation = 0
        if self.neighbours:
            for neighbour in self.neighbours:
                delta_orientation = neighbour.orientation - self.orientation
                average_delta_orientation = delta_orientation if delta_orientation <= 180 else delta_orientation-360
            average_delta_orientation /= len(self.neighbours)
        return (abs(average_delta_orientation),average_delta_orientation)


    def _get_recommendation_centering(self):

        if not self.neighbours:
            return (0,0)
        else:
            average_position = [0,0]
            for neighbour in self.neighbours:
                neighbour_relative_position = (
                    _find_shortest_path(self.position[0], neighbour.position[0], self.bounds[1], self.bounds[0]),
                    _find_shortest_path(self.position[1], neighbour.position[1], self.bounds[3], self.bounds[2]))
                average_position[0] += neighbour_relative_position[0]
                average_position[1] += neighbour_relative_position[1]
            average_position[0] /= len(self.neighbours)+1
            average_position[1] /= len(self.neighbours)+1
            orientation_position = sign(average_position[1]) * angle_between_vectors((1,0),average_position)
            orientation_change = (orientation_position - self.orientation)
            recommended_orientation_change = orientation_change
            recommendation_severity = distance_between_points((0,0),average_position) * 10
            return (recommendation_severity,recommended_orientation_change)


    @property
    def neighbours(self):
        '''
        If needs updating, updates nearest neighbours from boidcollection
        :return: dict of neighbour:distance
        '''
        if self._neighbours_need_updating:
            displacements = self.collection.get_displacements()[self]
            self._neighbours = {}
            for boid, displacement in displacements.items():
                if displacement < self.vision_range and self._in_vision_angle(boid):
                    self._neighbours[boid] = displacement
            self._neighbours_need_updating = False
        return self._neighbours


    def _in_vision_angle(self, boid):
        boid_relative_position = (self.position[0] + _find_shortest_path(self.position[0], boid.position[0], self.bounds[1],self.bounds[0]),
                         self.position[1] + _find_shortest_path(self.position[1], boid.position[1], self.bounds[3],self.bounds[2]))
        theta = self._angle_from_me_to_position(boid_relative_position)
        return True if abs(theta) <= self.vision_angle else False


    def _angle_from_me_to_position(self,position):
        '''
        Returns abs(theta) from Boid to position
        :param position: position in absolute space
        :return: angle theta, in degrees
        '''
        relative_position = (position[0] - self.position[0], position[1] - self.position[1])
        heading = self.get_heading(False)
        relative_heading = (heading[0] - self.position[0], heading[1] - self.position[1])
        return angle_between_vectors(relative_position,relative_heading)


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
        self.position = adjust_position_for_boundaries(self.position,self.bounds,self.tolerance)


    def _update_movement_vector(self):
        '''
        Internal function to update the movement vector
        '''
        self._movement_vector = [self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)]


    def _new_position(self):
        self._neighbours_need_updating = True


    def get_heading(self,adjusted=True):
        '''
        Returns the heading (x_heading,y_heading) based off vision_range
        :return: (x_heading,y_heading)
        '''
        x_heading = self.position[0] + (self.vision_range * math.cos(self.angle))
        y_heading = self.position[1] + (self.vision_range * math.sin(self.angle))
        heading = (x_heading, y_heading)
        if adjusted:
            heading = adjust_position_for_boundaries(heading,self.bounds,self.tolerance)
        return heading