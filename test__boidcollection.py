import random
import pytest
from _boidcollection import BoidCollection


@pytest.fixture
def boidcollection():
    random.seed(1)
    return BoidCollection()


@pytest.mark.parametrize('number,expected',((None,1),(1,1),(10,10),(100,100)))
def test_add(boidcollection,number,expected):
    boidcollection.add(number)
    assert len(boidcollection.boids) == expected


def test_add_collection(boidcollection):
    boidcollection.add()
    for boid in boidcollection.boids:
        assert boid.collection == boidcollection


@pytest.mark.parametrize('position1,position2,expected_value',(
        ((3,4),(6,8),5),
        ((6,8),(3,4),5),
        ((639,479),(7,5),10)
))
def test_update_displacements(boidcollection,position1,position2,expected_value):
    b1 = boidcollection.add(position=position1,bounds=(0,640,0,480))[0]
    b2 = boidcollection.add(position=position2,bounds=(0,640,0,480))[0]
    boidcollection._update_displacements()
    print(boidcollection.displacements)
    assert boidcollection.displacements[b1][b2] == pytest.approx(expected_value)