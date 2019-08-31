import random
import pytest
from _boidcollection import BoidCollection, _find_shortest_path

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


@pytest.mark.parametrize('x1,x2,xmin,xmax,expected_result',(
        (790,10,0,800,20),
        (10,790,0,800,20),
        (10,10,0,800,0),
        (10,20,0,800,10),
        (790,10,10,800,10)
))
def test_find_shortest_path(x1,x2,xmin,xmax,expected_result):
    assert _find_shortest_path(x1,x2,xmax,xmin) == expected_result
