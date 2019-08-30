import pytest
import random
from _boid import Boid, DEFAULT_SIZE


@pytest.fixture
def boid():
    random.seed(1)
    return Boid(size=20,palette=(-1000,128,1000))


def test_orientation(boid):
    assert boid.orientation < 360 and boid.orientation >= 0


def test_palette(boid):
    assert boid.colour[0] == 0
    assert boid.colour[1] > 0 and boid.colour[1] < 255
    assert boid.colour[2] == 255


@pytest.mark.parametrize('orientation,speed,expected_x,expected_y',(
        (0,10,10,0),
        (90,10,0,10),
        (180,10,-10,0),
        (270,20,0,-20)))
def test_movement_vector(boid,orientation,speed,expected_x,expected_y):
    boid.orientation = orientation
    boid.speed = speed
    boid._update_movement_vector()
    assert boid._movement_vector[0] == pytest.approx(expected_x)
    assert boid._movement_vector[1] == pytest.approx(expected_y)


@pytest.mark.parametrize('orientation,speed,expected_x,expected_y',(
        (0,10,10,0),
        (90,10,0,10),
        (180,10,790,0),
        (270,20,0,580)))
def test_tick(boid,orientation,speed,expected_x,expected_y):
    boid.orientation = orientation
    boid.speed = speed
    boid.position = [0,0]
    boid.bounds = (0,800,0,600)
    boid.tick()
    assert boid.position[0] == pytest.approx(expected_x)
    assert boid.position[1] == pytest.approx(expected_y)


@pytest.mark.parametrize('x,y,orientation,width,length,expected_vertices',(
        (0,0,0,20,40,(20,0,-20,-10,-20,10)),
        (0,0,90,20,40,(0,20,10,-20,-10,-20)),
        (0,0,180,20,40,(-20,0,20,10,20,-10)),
        (0,0,270,20,40,(0,-20,-10,20,10,20))
))
def test_vertices(boid,x,y,orientation,width,length,expected_vertices):
    boid.orientation = orientation
    boid.width = width
    boid.length = length
    boid.position = [x,y]
    boid.update_offsets()
    v = boid.get_vertices()
    for i,result in enumerate(expected_vertices):
        assert v[i] == pytest.approx(result)
