import pytest

from _boidlogic import Priority


@pytest.mark.parametrize('avoid,match,centre,allowed_change,expected_result',(
        ((0,0),(0,0),(0,0),2,0),
        ((0,0),(0,0),(1,1),2,1),
        ((0,0),(2,-1),(1,3),2,0),
        ((0,0),(1,-1),(2,3),2,2),
        ((10000,-2),(20,200),(200,2000),2,-2),
))
def test_priority_from_recommendations(avoid,match,centre,allowed_change,expected_result):
    priority = Priority(allowed_change)
    recommendations = (avoid,match,centre)
    assert priority.from_recommendations(recommendations) == expected_result