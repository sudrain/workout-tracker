import pytest
from utils import parse_pace


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
