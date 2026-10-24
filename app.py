
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st


st.title("🎮 WordQuest")
st.subheader("✨ Daily Word Challenge")
st.write("Guess the secret five-letter word!")
st.write("🟩 Correct place | 🟨 Wrong place | ⬜ Not in word")


# Load words in the same order as wordquest.py
with open("words.txt", "r", encoding="utf-8") as file:
    all_words = file.read().splitlines()

words = list(dict.fromkeys(
    word.strip().lower()
    for word in all_words
    if len(word.strip()) == 5 and word.strip().isalpha()
))

valid_words = set(words)

if not words:
    st.error("No valid five-letter words found in words.txt.")
    st.stop()


# Choose today's word using the same logic as wordquest.py
today=datetime.now(ZoneInfo("Asia/Kolkata")).date()
day_number = today.year * 10000 + today.month * 100 + today.day
random.seed(day_number)
answer = random.choice(words)


# Save progress for this browser session
if "guesses" not in st.session_state:
    st.session_state.guesses = []

if "finished" not in st.session_state:
    st.session_state.finished = False

if "won" not in st.session_state:
    st.session_state.won = False


# Feedback function
def show_feedback(guess, answer):
    feedback = ["⬜"] * 5
    remaining = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = "🟩"
            remaining[i] = None

    for i in range(5):
        if feedback[i] != "🟩" and guess[i] in remaining:
            feedback[i] = "🟨"
            remaining[remaining.index(guess[i])] = None

    return " ".join(feedback)


# Display previous guesses
for old_guess in st.session_state.guesses:
    st.write(old_guess.upper(), show_feedback(old_guess, answer))


# Guess input
guess = st.text_input(
    "Enter your five-letter guess:",
    key="guess_input",
    disabled=st.session_state.finished
)

if st.button("Submit Guess", disabled=st.session_state.finished):
    guess = guess.strip().lower()

    if len(guess) != 5 or not guess.isalpha():
        st.warning("Enter exactly five letters.")

    elif guess not in valid_words:
        st.warning("That word isn't in our word list.")

    elif guess in st.session_state.guesses:
        st.warning("You already tried that word!")

    else:
        st.session_state.guesses.append(guess)

        if guess == answer:
            st.session_state.won = True
            st.session_state.finished = True

        elif len(st.session_state.guesses) >= 6:
            st.session_state.finished = True

        st.rerun()


# Game status
if st.session_state.won:
    st.success("🎉 You guessed today's word!")

elif st.session_state.finished:
    st.error(f"Game over! Today's word was {answer.upper()}.")

else:
    remaining = 6 - len(st.session_state.guesses)
    st.write(f"Attempts remaining: {remaining}/6")
