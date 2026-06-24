import pytest

from logic_utils import (
    get_range_for_difficulty,
    get_attempt_limit,
    parse_guess,
    check_guess,
    update_score,
)


# ---------- check_guess ----------

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_returns_message():
    _, message = check_guess(50, 50)
    assert isinstance(message, str) and message != ""

def test_check_guess_boundary_off_by_one():
    assert check_guess(51, 50)[0] == "Too High"
    assert check_guess(49, 50)[0] == "Too Low"


# ---------- get_range_for_difficulty ----------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 500)

def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)


# ---------- get_attempt_limit ----------

def test_attempts_easy():
    assert get_attempt_limit("Easy") == 6

def test_attempts_normal():
    assert get_attempt_limit("Normal") == 8

def test_attempts_hard():
    assert get_attempt_limit("Hard") == 10

def test_attempts_unknown_defaults_to_eight():
    assert get_attempt_limit("Nightmare") == 8


# ---------- parse_guess ----------

def test_parse_guess_valid():
    ok, value, err = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_strips_whitespace():
    ok, value, _ = parse_guess("  17  ", 1, 100)
    assert ok is True
    assert value == 17

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_whitespace_only():
    ok, _, err = parse_guess("   ", 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_none():
    ok, _, err = parse_guess(None, 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_rejects_decimal():
    ok, value, err = parse_guess("3.5", 1, 100)
    assert ok is False
    assert value is None
    assert "whole number" in err.lower()

def test_parse_guess_rejects_non_numeric():
    ok, _, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_below_range():
    ok, _, err = parse_guess("0", 1, 100)
    assert ok is False
    assert "between" in err.lower()

def test_parse_guess_above_range():
    ok, _, err = parse_guess("101", 1, 100)
    assert ok is False
    assert "between" in err.lower()

def test_parse_guess_at_lower_bound():
    ok, value, _ = parse_guess("1", 1, 100)
    assert ok is True
    assert value == 1

def test_parse_guess_at_upper_bound():
    ok, value, _ = parse_guess("100", 1, 100)
    assert ok is True
    assert value == 100

def test_parse_guess_negative_number():
    ok, _, err = parse_guess("-5", 1, 100)
    assert ok is False
    assert err is not None


# ---------- update_score ----------

def test_score_win_first_attempt():
    # 100 - 10*(1-1) = 100
    assert update_score(0, "Win", 1) == 100

def test_score_win_second_attempt():
    # 100 - 10*(2-1) = 90
    assert update_score(0, "Win", 2) == 90

def test_score_win_floor_is_ten():
    # On attempt 20, raw would be 100 - 190 = -90, but floor is 10
    assert update_score(0, "Win", 20) == 10

def test_score_win_at_floor_boundary():
    # Attempt 10: 100 - 90 = 10 exactly
    assert update_score(0, "Win", 10) == 10

def test_score_win_adds_to_existing_score():
    assert update_score(50, "Win", 1) == 150

def test_score_too_high_subtracts_five():
    assert update_score(100, "Too High", 3) == 95

def test_score_too_low_subtracts_five():
    assert update_score(100, "Too Low", 3) == 95

def test_score_can_go_negative():
    assert update_score(0, "Too Low", 1) == -5

def test_score_unknown_outcome_unchanged():
    assert update_score(42, "Something Weird", 1) == 42