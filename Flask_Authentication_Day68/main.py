from flask import Flask, render_template, request, url_for, redirect, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from pathlib import Path
from sqlalchemy.exc import NoResultFound, IntegrityError


# Initiating Flask App with instance path
current_directory = Path("G:/Video Lectures/100DaysToCode/pythonProject/Day68_Flask_Authentication")
app = Flask(__name__, instance_path=str(current_directory.resolve()))
app.secret_key = '7ed6754ed4d6cad7fb82c18c77013cb6f98a9121d907376f63ac5b91e9a5a1df'

# Initiating Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


# # CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # def __int__(self, email, name, password):
    #     self.email = email
    #     self.name = name
    #     self.password = password
    #
    # def __repr__(self):
    #     return f"<{self.name}>"


# Line below only required once, when creating DB.
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    try:
        cur_user = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar_one()
    except NoResultFound:
        cur_user = None
    return cur_user


@app.route('/')
def home():
    return render_template("index.html", name=session["name"])


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            email=request.form['email'],
            name=request.form["name"],
            password=generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Email already registered. Please login", category="error")
            return redirect(url_for('login'))

        # login the registered user so that he can access secrets page
        session['name'] = user.name
        login_user(user)
        flash("Registered, and Logged in")
        return redirect(url_for('secrets'))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['password']
        try:
            user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one()
        except NoResultFound:
            flash("Your Email ID is not registered.", category="error")
            return redirect(url_for('login'))

        if check_password_hash(user.password, user_password):
            login_user(user)
            flash("Successfully logged in", category="success")
            session['name'] = user.name
            return redirect(url_for('secrets'))
        else:
            flash("Password is not correct!")
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    user_name = request.args.get("name")
    return render_template("secrets.html", name=session['name'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.get('/download')
@login_required
def download():
    return send_from_directory("static", "files/cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
