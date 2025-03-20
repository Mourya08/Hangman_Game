from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

WORDS = ["apple", "grape", "table", "chair", "house", "robot", "pencil", "banana", "cloud", "train",  
         "laptop", "window", "rocket", "guitar", "planet", "python", "coding", "silver", "bridge", "camera",  
         "elephant", "backpack", "airplane", "champion", "pyramid", "umbrella", "mystery", "diamond", "painting", "keyboard",  
         "astronaut", "knowledge", "lightning", "chocolate", "adventure", "waterfall", "microscope", "volleyball", "hurricane", "butterfly"]
games = {}

def initialize_game():
    word = random.choice(WORDS)
    first_letter = word[0]
    hidden_word = [first_letter] + ["_" for _ in word[1:]]  # Always reveal the first letter
    return {
        "word": word,
        "hidden_word": hidden_word,
        "attempts_left": 6,
        "guessed_letters": [first_letter]  # Track guessed letters, including the first letter
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start_game():
    game_id = len(games) + 1
    games[game_id] = initialize_game()
    return jsonify({"game_id": game_id, **games[game_id]})

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.json
    game_id = data["game_id"]
    letter = data["letter"].lower()

    if game_id not in games:
        return jsonify({"error": "Invalid game ID"}), 400

    game = games[game_id]

    if letter in game["guessed_letters"]:
        return jsonify({"message": "Letter already guessed", **game})

    game["guessed_letters"].append(letter)

    if letter in game["word"]:
        game["hidden_word"] = [
            game["word"][i] if game["word"][i] == letter or game["hidden_word"][i] != "_" else game["hidden_word"][i]
            for i in range(len(game["word"]))
        ]
    else:
        game["attempts_left"] -= 1

    game_status = "won" if "_" not in game["hidden_word"] else "lost" if game["attempts_left"] == 0 else "playing"

    return jsonify({"status": game_status, **game})


if __name__ == '__main__':
    app.run(debug=True)
