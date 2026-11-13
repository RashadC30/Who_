import http.server
import json
import random
from countries_data import world  # Assuming 'world' is defined in a separate module named 'countries'

# Store game state in memory
game_state = {
    "username": "",
    "score": 0,
    "guesses": 10,
    "remaining_world": {},
    "target_country": None,
    "last_country": None
}

question_templates = {
    "capital": "Which country has the capital city '{}'?",
    "dish": "Which country is famous for the dish '{}'?",
    "language": "Which country has '{}' as its national language?",
    "region": "Which country is located in '{}'?",
    "flag": "Which country has a flag with the colors '{}'?"
}

def pick_next_question():
    remaining = list(game_state["remaining_world"].keys())
    if not remaining:
        return None
    
    if len(remaining) > 1 and game_state["last_country"] in remaining:
        choices = [c for c in remaining if c != game_state["last_country"]]
        target = random.choice(choices)
    else:
        target = random.choice(remaining)
        
    game_state["target_country"] = target
    game_state["last_country"] = target
    
    clue_type = random.choice(list(question_templates.keys()))
    country_data = game_state["remaining_world"][target]
    return question_templates[clue_type].format(country_data[clue_type])

class GameHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Endpoint to read scores.txt
        if self.path == "/scores":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            try:
                with open("scores.txt", "r") as f:
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.wfile.write(b"No scores yet!")
        else:
            # Serve index.html and style.css automatically
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        response = {}

        if self.path == "/start":
            game_state["username"] = post_data.get("username", "Player")
            game_state["score"] = 0
            game_state["guesses"] = 10
            game_state["remaining_world"] = dict(world)
            game_state["last_country"] = None
            
            question = pick_next_question()
            response = {
                "question": question,
                "guesses": game_state["guesses"],
                "score": game_state["score"],
                "remaining": len(game_state["remaining_world"])
            }

        elif self.path == "/guess":
            guess = post_data.get("guess", "").strip().title()
            target = game_state["target_country"]
            game_state["guesses"] -= 1

            if guess == target:
                game_state["score"] += 1
                del game_state["remaining_world"][target]
                message = f"Correct! Your score is now {game_state['score']}."
            else:
                message = f"Wrong! The answer was {target}."

            game_over = len(game_state["remaining_world"]) == 0 or game_state["guesses"] <= 0
            next_question = None

            if game_over:
                with open("scores.txt", "a") as f:
                    f.write(f"{game_state['username']}: {game_state['score']}\n")
            else:
                next_question = pick_next_question()

            response = {
                "message": message,
                "question": next_question,
                "guesses": game_state["guesses"],
                "score": game_state["score"],
                "remaining": len(game_state["remaining_world"]),
                "game_over": game_over
            }

        elif self.path == "/hint":
            target = game_state["target_country"]
            response = {"hint": game_state["remaining_world"][target]}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    print("Server running at http://localhost:8000")
    http.server.HTTPServer(("localhost", 8000), GameHandler).serve_forever()
