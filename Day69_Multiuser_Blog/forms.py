from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import InputRequired, URL, Length, Email, EqualTo
from flask_ckeditor import CKEditorField


# # WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired(), Length(min=1, max=250)])
    email = EmailField(label="Email", validators=[InputRequired(), Length(min=1, max=250), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField(label="Confirm Password",
                                     validators=[InputRequired(), EqualTo('password', message="Passwords Don't Match")])
    submit = SubmitField(label="Sign Me Up!")


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[InputRequired(), Length(min=1, max=250), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(), Length(min=8, max=100)])
    submit = SubmitField(label="Log Me In!")


class CommentForm(FlaskForm):
    comment = CKEditorField(label="Comment")
    submit = SubmitField(label="Submit")