
import random
from datetime import date


# Load words in their original file order
with open("words.txt", "r", encoding="utf-8") as file:
    all_words = file.read().splitlines()

words = list(dict.fromkeys(
    word.strip().lower()
    for word in all_words
    if len(word.strip()) == 5 and word.strip().isalpha()
))

valid_words = set(words)

if not words:
    print("No valid five-letter words found in words.txt.")
    raise SystemExit

# Choose today's word
random.seed(date.today().toordinal())
answer = random.choice(words)


def show_feedback(guess, answer):
    feedback = ["⬜"] * 5
    remaining = list(answer)

    # Correct letters in correct positions
    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = "🟩"
            remaining[i] = None

    # Correct letters in wrong positions
    for i in range(5):
        if feedback[i] != "🟩" and guess[i] in remaining:
            feedback[i] = "🟨"
            remaining[remaining.index(guess[i])] = None

    return " ".join(feedback)


def play_game():
    print("\n🎮 Welcome to WordQuest!")
    print("Guess the five-letter word.")
    print("🟩 Correct place | 🟨 Wrong place | ⬜ Not in word")
    print("You have 6 attempts.\n")

    for attempt in range(1, 7):
        guess = input(f"Attempt {attempt}/6: ").strip().lower()

        if len(guess) != 5 or not guess.isalpha():
            print("Enter exactly five letters.\n")
            continue

        if guess not in valid_words:
            print("That word isn't in our word list.\n")
            continue

        print(show_feedback(guess, answer))

        if guess == answer:
            print("🎉 Correct! You guessed today's word!")
            return

    print(f"Game over! Today's word was {answer.upper()}.")


if __name__ == "__main__":
    play_game()
