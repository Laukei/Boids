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