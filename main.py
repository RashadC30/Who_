import random
from countries_data import world  # Assuming 'world' is defined in a separate module named 'countries'

# Keep your existing 'world' dictionary above this line
score = 0
guesses = 10
username = input("Enter your username: ")
options = input("A. Start Game \nB. See Scores\n")

if options.lower() == "b" or options.lower() == "see scores":
    with open("scores.txt", "r") as file:
        print(file.read())
else:
    print("Welcome to the Country Guessing Game!")
    print(f"You have {guesses} total guesses to get all {len(world)} countries right!")

    question_templates = {
        "capital": "Which country has the capital city '{}'?",
        "dish": "Which country is famous for the dish '{}'?",
        "language": "Which country has '{}' as its national language?",
        "region": "Which country is located in '{}'?",
        "flag": "Which country has a flag with the colors '{}'?"
    }

    last_country = None

    while guesses > 0 and len(world) > 0:
        # 1. Get all remaining unguessed countries
        remaining_countries = list(world.keys())

        # 2. Pick a different random country than the last turn (when more than 1 remains)
        if len(remaining_countries) > 1 and last_country in remaining_countries:
            choices = [c for c in remaining_countries if c != last_country]
            target_country = random.choice(choices)
        else:
            target_country = random.choice(remaining_countries)

        last_country = target_country
        country_data = world[target_country]

        # 3. Ask a random question about this target country
        clue_type = random.choice(list(question_templates.keys()))
        question = question_templates[clue_type].format(country_data[clue_type])

        print(f"\nGuesses left: {guesses} | Countries left: {len(world)}")
        print(f"QUESTION: {question}")
        guessed_country = input("Guess the country (or type 'hint' for clues, 'exit' to quit): ")

        if guessed_country.lower() == "exit":
            print("Thanks for playing!")
            break

        elif guessed_country.lower() == "hint":
            print("\n--- COUNTRY HINT ---")
            print(f"Flag Colors: {country_data['flag']}")
            print(f"National Language: {country_data['language']}")
            print(f"Most Famous Dish: {country_data['dish']}")
            print(f"Local Region: {country_data['region']}")
            print(f"Capital City: {country_data['capital']}\n")
            continue

        # Deduct 1 from the 10-guess limit on every guess attempt
        guesses -= 1
        guessed_country = guessed_country.strip().title()

        if guessed_country == target_country:
            score += 1
            del world[target_country]
            print(f"Correct! Your score is now {score}.")
        else:
            print(f"Wrong! The answer was {target_country}.")

    # Check whether the player cleared the board or ran out of guesses
    if len(world) == 0:
        print("\nVictory! You guessed every country on the list!")
    elif guesses == 0:
        print("\nOut of guesses! Better luck next time.")

    # Save final score to scores.txt
    with open("scores.txt", "a") as file:
        file.write(f"{username}: {score}\n")
    print(f"Game Over! Final Score: {score}")
