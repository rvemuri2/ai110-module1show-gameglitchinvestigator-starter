def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of attempts allowed for a given difficulty."""
    limits = {
        "Easy": 6,
        "Normal": 8,
        "Hard": 10,
    }
    return limits.get(difficulty, 8)


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate it is within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    # Reject decimals outright rather than silently truncating.
    if "." in raw:
        return False, None, "Enter a whole number."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome is one of: "Win", "Too High", "Too Low".
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update score based on outcome and attempt number (1-indexed).

    - Win: 100 points on attempt 1, decreasing by 10 each attempt, floor of 10.
    - Wrong guess (Too High / Too Low): -5 points.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score