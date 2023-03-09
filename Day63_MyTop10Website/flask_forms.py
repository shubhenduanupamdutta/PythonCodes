from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FloatField, StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from database_classes import Movie


class RateMovieForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g. 7.6",
                        validators=[InputRequired(), NumberRange(min=0, max=10)], render_kw={"class": "mb-4"})
    review = TextAreaField(label="Your Review", render_kw={"rows": "5", "class":"mb-4"})
    submit = SubmitField(label="Change", render_kw={"class":"w-100"})


class AddMovie(FlaskForm):
    movie_name = StringField(label="Movie Title", validators=[InputRequired()], render_kw={"class": "mb-4"})
    submit = SubmitField(label="Add Movie", render_kw={"class": "w-100 btn btn-primary"})

