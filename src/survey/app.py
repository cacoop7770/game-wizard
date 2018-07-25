from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/survey", methods=["POST"])
def survey():
    """
    Takes in a list of products and return a json with the user profile as well as
    a list of games recommended=
    """
    result = {
        "user_profile": {
            "id": 1,
            "fantasy": 0.5,
            "exploration": 0.5,
            "competence": 0.3
        },
        "games": {
            "fantasy": ["1", "2", "3"],
            "exploration": ["2", "5", "6"]
        }
    }

    req_data = request.get_json()
    result.update({"initial_games": req_data})

    return json.dumps(result)

if __name__ == "__main__":
    app.run()
