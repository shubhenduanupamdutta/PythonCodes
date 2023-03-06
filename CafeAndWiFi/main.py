from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import os
import csv

app = Flask(__name__)
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

csv_file_path = os.path.abspath(os.path.join(os.getcwd(), 'cafe-data.csv'))


def ratings_list(symbol: str) -> list:
    choices = ['✘']
    for i in range(1, 6):
        choice = ""
        for j in range(i):
            choice += symbol
        choices.append(choice)
    return choices


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()], render_kw={"class":"mb-3"})
    location_url = URLField(label='Location', validators=[DataRequired(), URL()], render_kw={"class":"mb-3"})
    open_at = StringField(label="Open", validators=[DataRequired()], render_kw={"class":"mb-3"})
    close_at = StringField(label="Close", validators=[DataRequired()], render_kw={"class":"mb-3"})
    coffee_quality = SelectField(label="Coffee", choices=ratings_list('☕️'), default="☕️", render_kw={"class":"mb-3"})
    wifi_strength = SelectField(label="Wifi", choices=ratings_list('💪'), default="✘", render_kw={"class":"mb-3"})
    power_sockets = SelectField(label="Power", choices=ratings_list('🔌'), default="✘", render_kw={"class":"mb-3"})
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

def read_cafe_csv(file_path: os.path.abspath):
    with open(file_path, encoding="utf-8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return list_of_rows


def write_to_csv(file: os.path.abspath, cafe_data: CafeForm):
    row_entry = ["\n" + str(cafe_data.cafe.data), cafe_data.location_url.data, cafe_data.open_at.data,
                 cafe_data.close_at.data, cafe_data.coffee_quality.data, cafe_data.wifi_strength.data,
                 cafe_data.power_sockets.data]
    with open(file, 'a', encoding="utf-8") as filename:
        filename.write(",".join(map(str, row_entry)))


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        write_to_csv(csv_file_path, form)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    return render_template('cafes.html', cafes=read_cafe_csv(csv_file_path))


if __name__ == '__main__':
    app.run(debug=True)
