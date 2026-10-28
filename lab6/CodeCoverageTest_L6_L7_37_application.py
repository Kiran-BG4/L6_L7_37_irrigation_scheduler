import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# should_irrigate tests

def test_wet_soil_no_irrigation():
    assert should_irrigate(70, 0, "seedling") is False

def test_rain_no_irrigation():
    assert should_irrigate(30, 10, "seedling") is False

def test_seedling_needs_water():
    assert should_irrigate(30, 0, "seedling") is True

def test_seedling_moisture_boundary():
    assert should_irrigate(45, 0, "seedling") is False

def test_flowering_needs_water():
    assert should_irrigate(50, 0, "flowering") is True

def test_flowering_does_not_need_water():
    assert should_irrigate(55, 0, "flowering") is False

def test_other_stage_rain_boundary():
    assert should_irrigate(30, 5, "mature") is False

def test_other_stage_needs_water():
    assert should_irrigate(30, 0, "mature") is True

def test_other_stage_moisture_boundary():
    assert should_irrigate(40, 0, "mature") is False


# water_volume tests

def test_seedling_volume():
    assert water_volume(10, "seedling", 20) == 20

def test_flowering_volume():
    assert water_volume(10, "flowering", 20) == 50

def test_other_stage_volume():
    assert water_volume(10, "mature", 20) == 40

def test_high_temperature():
    assert water_volume(10, "seedling", 36) == 30

def test_low_temperature():
    assert water_volume(10, "seedling", 9) == 10

def test_temperature_boundaries():
    assert water_volume(10, "seedling", 10) == 20
    assert water_volume(10, "seedling", 35) == 20

def test_zero_area():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)

def test_negative_area():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-5, "seedling", 20)


# schedule tests

def test_schedule_skips_zone():
    zones = [("A", 10, 70, 0, "seedling", 20)]
    assert schedule(zones, 100) == []

def test_schedule_adds_zone():
    zones = [("A", 10, 30, 0, "seedling", 20)]
    assert schedule(zones, 100) == ["A"]

def test_schedule_stops_when_budget_insufficient():
    zones = [
        ("A", 10, 30, 0, "seedling", 20),
        ("B", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 30) == ["A"]

def test_schedule_skips_then_adds():
    zones = [
        ("A", 10, 70, 0, "seedling", 20),
        ("B", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 100) == ["B"]

def test_schedule_empty():
    assert schedule([], 100) == []

def test_schedule_exact_budget():
    zones = [
        ("A", 10, 30, 0, "seedling", 20),
        ("B", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 40) == ["A", "B"]
