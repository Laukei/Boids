import random
import pytest
from _boid import Boid, _find_shortest_path, angle_between_vectors


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
    boid._update_offsets()
    v = boid.get_vertices()
    for i,result in enumerate(expected_vertices):
        assert v[i] == pytest.approx(result)


@pytest.mark.parametrize('x1,x2,xmin,xmax,expected_result',(
        (790,10,0,800,20),
        (10,790,0,800,-20),
        (10,10,0,800,0),
        (10,20,0,800,10),
        (790,10,10,800,10)
))
def test_find_shortest_path(x1,x2,xmin,xmax,expected_result):
    assert _find_shortest_path(x1,x2,xmax,xmin) == pytest.approx(expected_result)


@pytest.mark.parametrize('position,orientation,vision_range,bounds,expected_result',(
        ([0,0],0,50,(0,640,0,480),[50,0]),
        ([0,0],90,50,(0,640,0,480),[0,50]),
        ([630,470],45,50,(0,640,0,480),[-10 + ((50**2)/2)**0.5,-10 + ((50**2)/2)**0.5]),
        ([10,10],225,50,(0,640,0,480),[650 - ((50**2)/2)**0.5,490 - ((50**2)/2)**0.5])
))
def test_get_heading(boid,position,orientation,vision_range,bounds,expected_result):
    boid.position = position
    boid.orientation = orientation
    boid.vision_range = vision_range
    boid.bounds = bounds
    assert boid.get_heading() == pytest.approx(expected_result)


@pytest.mark.parametrize('pos1,pos2,vision_angle,orientation,expected_result',(
        ((0,0),(1,0),135,0,True),
        ((0,0),(-1,0),135,0,False),
        ((0,0),(0,1),135,90,True),
        ((0,0),(0,-1),135,90,False),
        ((200,200),(201,200),135,0,True),
        ((200,200),(199,200),135,0,False),
        ((200,200),(200,201),135,90,True),
        ((200,200),(200,199),135,90,False)
))
def test__can_see(pos1,pos2,vision_angle,orientation,expected_result):
    boid1 = Boid(position=pos1,vision_angle=vision_angle,orientation=orientation)
    boid2 = Boid(position=pos2)
    assert boid1._in_vision_angle(boid2) == expected_result


@pytest.mark.parametrize('pos1,pos2,orientation,expected_result',(
        ((0,0),(1,1),0,45),
        ((0,1),(1,0),0,45),
        ((0,0),(-1,-1),0,135),
        ((0,0),(0,1),90,0),
        ((0,0),(0,-1),90,180),
        ((10,11),(11,10),0,45),
        ((200,200),(201,200),0,0),
        ((200,200),(199,200),0,180),
        ((200,200),(200,201),90,0),
        ((200,200),(200,199),90,180),
        ((200,200),(200,199),180,90)
))
def test__angle_from_me_to_position(pos1,pos2,orientation,expected_result):
    boid = Boid(position=pos1,orientation=orientation)
    assert boid._angle_from_me_to_position(pos2) == pytest.approx(expected_result)


@pytest.mark.parametrize('v1,v2,expected_result',(
        ((0,1),(0,1),0),
        ((1,0),(-1,0),180),
        ((0,1),(0,-1),180),
        ((0,1),(1,0),90)
))
def test_angle_between_vectors(v1,v2,expected_result):
    assert angle_between_vectors(v1,v2) == pytest.approx(expected_result)