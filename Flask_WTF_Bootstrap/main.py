from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "FormValidationKey_5641687416341687431"


class LoginForm(FlaskForm):
    # name = StringField(label='Name')
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(min=5)], render_kw={"class": "form-fields mb-3"})
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)], render_kw={"class": "form-fields mb-3"})
    submit = SubmitField(label="Log In", render_kw={"class": "btn btn-primary btn-lg"})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
