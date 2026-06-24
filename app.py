import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    get_attempt_limit,
    parse_guess,
    check_guess,
    update_score,
)


def reset_game(low: int, high: int):
    """Reset all game state for a fresh round."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Initialize state on first load.
if "secret" not in st.session_state:
    reset_game(low, high)

# If the user changes difficulty mid-game, reset so the secret matches the range.
if st.session_state.get("difficulty") != difficulty:
    reset_game(low, high)
    st.session_state.difficulty = difficulty

st.subheader("Make a guess")

# FIX: Moved the text input and buttons up here, ABOVE the info box and debug
# expander, so that the submit handler can run before anything that displays
# attempts/score/history gets rendered.
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Handle "New Game" before processing a submit, so a stale submit click
# doesn't get processed against a freshly reset game state.
if new_game:
    reset_game(low, high)
    st.session_state.difficulty = difficulty
    st.success("New game started.")
    st.rerun()

# FIX: This entire submit-handling block was moved UP from the bottom of the
# file. The original bug was that attempts/score/history were rendered before
# this block mutated them, so the UI showed stale values for one rerun cycle.
# Now state is updated BEFORE anything reads it.
submit_error = None
hint_message = None
win_message = None
lose_message = None
did_win = False

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        submit_error = err
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)
        if show_hint:
            hint_message = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            did_win = True
            win_message = (
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            lose_message = (
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

# FIX: Info box now renders AFTER the submit handler, so "Attempts left"
# reflects the guess that was just submitted.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# FIX: Debug expander also moved below the submit handler so attempts/score/
# history shown here are current, not stale by one rerun.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX: Feedback messages (error, hint, balloons, win/lose) are deferred into
# local variables above and rendered here, so they appear alongside the
# freshly updated numbers instead of next to stale ones.
if submit_error:
    st.error(submit_error)
if hint_message:
    st.warning(hint_message)
if did_win:
    st.balloons()
if win_message:
    st.success(win_message)
if lose_message:
    st.error(lose_message)

# FIX: Game-over guard now checks "not (did_win or lose_message)" so the
# winning/losing message from the CURRENT guess still shows on this rerun.
# Originally, st.stop() would have swallowed it.
if st.session_state.status != "playing" and not (did_win or lose_message):
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")