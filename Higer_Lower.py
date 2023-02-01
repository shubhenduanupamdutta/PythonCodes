from flask import Flask
# from markupsafe import escape
import random

app = Flask(__name__)


@app.route("/")
def guess_a_number():
    return "<h1>Guess a number between 1 and 10 (including both): </h1>" \
           "<img src='https://media.giphy.com/media/hTrCbhPoQEcCT18JLf/giphy.gif'>" \
           "<h2>Change to URL to show your number, like current_url/number"


random_number = random.randint(1, 10)


@app.route("/<int:guessed_number>")
def show_result(guessed_number):
    if guessed_number > random_number:
        return "<h1 style='color: red;'> Too high, try again!</h1>" \
               "<img src='https://media.giphy.com/media/Js7cqIkpxFy0bILFFA/giphy.gif'>"
    elif guessed_number < random_number:
        return "<h1 style='color: purple;'> Too low, try again!</h1>" \
               "<img src='https://media.giphy.com/media/KBJTi1lxDGrfPsl8Hf/giphy.gif'>"
    else:
        return "<h1 style='color: green;'> Correct! Good Job!</h1>" \
               "<img src='https://media.giphy.com/media/MAzunB1Ru6zAYlYgPD/giphy.gif'>"


if __name__ == "__main__":
    # Running in debug mode
    app.run(debug=True)
