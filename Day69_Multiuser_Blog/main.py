from flask import Flask, render_template, redirect, url_for, flash, session, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.exc import NoResultFound, IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from pathlib import Path
from functools import wraps

# initializing Flask app
cur_dir = Path()
app = Flask(__name__, instance_path=str(cur_dir.resolve()))
app.secret_key = 'f71fd9b450afda3c420cd068d3095a8d1a2b024d1679f8083293f0f04183fbef'

# initializing CKEditor
ckeditor = CKEditor()
ckeditor.init_app(app)

# initializing Bootstrap
bootstrap = Bootstrap5()
bootstrap.init_app(app)

# # CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy()
db.init_app(app)

# Initializing Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# initialize gravaar
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# # CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250), nullable=False)
    posts = relationship('BlogPost', back_populates='author')
    comments_by_author = relationship("Comment", back_populates='comment_writer')


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    comment_writer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_writer = relationship("User", back_populates="comments_by_author")
    date = db.Column(db.String(250))
    blog_post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    post = relationship("BlogPost", back_populates="comments")

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    try:
        cur_user = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar_one()
    except NoResultFound:
        cur_user = None
    return cur_user


def admin_only(function):
    @wraps(function)
    # @wraps(function) makes sure that queries like function.__name__ and such don't return wrapeer function
    def decorator_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)

        return function(*args, **kwargs)

    return decorator_function


@app.route('/')
def get_all_posts():
    posts = list(db.session.execute(db.select(BlogPost)).scalars())
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password=generate_password_hash(register_form.password.data, method="pbkdf2:sha256", salt_length=16)
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Email is already registered, please login!")
            return redirect(url_for('login'))

        login_user(new_user)
        session['name'] = register_form.name.data
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_email = login_form.email.data
        user_password = login_form.password.data
        try:
            user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one()
        except NoResultFound:
            flash("Wrong Email! You are not registered.")
            return redirect(url_for('login'))

        if check_password_hash(user.password, user_password):
            login_user(user)
            session['name'] = user.name
            return redirect(url_for('get_all_posts'))
        else:
            flash("Wrong Password!")
            return redirect(url_for('login'))

    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment!")
            return redirect(url_for('login'))
        elif comment_form.comment.data:
            new_comment = Comment(
                comment=comment_form.comment.data,
                comment_writer=current_user,
                comment_writer_id = current_user.id,
                date=datetime.today().strftime("%B %d, %Y"),
                blog_post_id=post_id

            )
            db.session.add(new_comment)
            db.session.commit()

    return render_template("post.html", post=requested_post, form=comment_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = {field: value for field, value in form.data.items() if field != 'submit' and field != "csrf_token"}
        new_post['date'] = date.today().strftime("%B %d, %Y")
        new_post['author'] = current_user
        new_post['author_id'] = int(current_user.id)
        post = BlogPost(**new_post)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.get("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.context_processor
def inject_variables():
    cur_year = datetime.now().year
    return dict(year=cur_year)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
