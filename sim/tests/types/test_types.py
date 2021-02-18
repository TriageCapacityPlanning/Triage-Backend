from sim.resources import types as t


def test_time_unit_breakdown_add():
    tub = t.TimeUnitBreakdown(0)
    assert tub.total == 0

    tub.add(1, 10)
    assert tub.total == 10

    tub.add(1, 20)
    assert tub.total == 20
