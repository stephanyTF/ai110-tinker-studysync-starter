"""
Tinker 1B, Part 1: write an assert-based pytest test for session_rating()
BEFORE you touch anything else. One test is started for you -- add at least
one more.
"""

from scoring import session_rating


def test_session_rating_boundary_90_is_great():
    assert session_rating(90) == "Great"

def test_session_rating_boundary_80_is_good():
    assert session_rating(80) == "Good"

#Part 3? Test session_rating() handling bad input.
def test_session_rating_negative_score():
    assert session_rating(-10) == "Skip" #works


def test_session_rating_boundary_over_100():
    assert session_rating(1000) == "Great" #works


def test_session_rating_boundary_decimal_is_good():
    assert session_rating(87.5) == "Good"  #can't take decimals since expects ints, TODO: convert to int or accept floats?

# TODO: add at least one more test, e.g. a boundary case for "Skip" (a score
# of 59) or the exact boundary for "Good" (a score of 80).
