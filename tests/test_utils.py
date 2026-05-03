import pytest

from utils import parse_pace, validate_strength_workout


def test_parse_pace_valid():
    assert parse_pace("5:30") == 330
    assert parse_pace("9:00") == 540
    assert parse_pace("10") == 600


def test_parse_pace_invalid():
    with pytest.raises(ValueError):
        parse_pace("abc")
    with pytest.raises(ValueError):
        parse_pace("10,2")
    with pytest.raises(ValueError):
        parse_pace("10:80")


@pytest.mark.parametrize(
    "bad_data, expected_error",
    [
        ({"exercises": []}, "exercises list must not be empty"),
        (
            {"exercises": [{"name": "pushup", "sets": [{"weight": 0, "reps": -1}]}]},
            "reps must be greater than 0",
        ),
        (
            {"exercises": [{"name": "pushup", "sets": [{"weight": -1, "reps": 23}]}]},
            "weight must not be negative",
        ),
        (
            {"exercises": [{"name": "", "sets": [{"weight": 0, "reps": 23}]}]},
            "exercise name must not be empty",
        ),
    ],
)
def test_invalid_workouts(bad_data, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        validate_strength_workout(bad_data)
