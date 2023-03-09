from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange


class AddBook(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired(), Length(max=250)], render_kw={"class": "mb-3"})
    author = StringField(label="Author", validators=[InputRequired(), Length(max=250)], render_kw={"class": "mb-3"})
    rating = FloatField(label="Rating", validators=[InputRequired(), NumberRange(min=0, max=10)],
                        render_kw={"class": "mb-3"})
    submit = SubmitField(label="Add Book", render_kw={"class": "add-book"})


class EditBook(FlaskForm):
    new_rating = FloatField(label="New rating", validators=[InputRequired(), NumberRange(min=0, max=10)],
                            render_kw={"class": "mb-3"})
    submit = SubmitField(label="Change", render_kw={"class": "change-rating"})