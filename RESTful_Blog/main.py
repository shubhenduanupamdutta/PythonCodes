from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from pathlib import Path
from datetime import datetime

# Initializing Flask App with instance_path of current_directory (needed for my configuration)
# change path according to you., Generate secret key
cur_dir = Path()
app = Flask(__name__, instance_path=str(cur_dir.resolve()))
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initializing ckeditor and Bootstrap5
ckeditor = CKEditor()
ckeditor.init_app(app)
bootstrap = Bootstrap5()
bootstrap.init_app(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# # CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    author = StringField("Your Name", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
@app.route("/home")
def get_all_posts():
    posts = list(db.session.execute(db.select(BlogPost).order_by(BlogPost.id)).scalars())
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = db.get_or_404(BlogPost, index)
    return render_template("post.html", post=requested_post)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post_to_edit = db.get_or_404(BlogPost, post_id)

    # This pre-populates the form to be rendered.
    edit_blog_form = CreatePostForm(
        title=post_to_edit.title,
        subtitle=post_to_edit.subtitle,
        date=post_to_edit.date,
        body=post_to_edit.body,
        author=post_to_edit.author,
        img_url=post_to_edit.img_url
    )
    if edit_blog_form.validate_on_submit():
        post_to_edit.title = edit_blog_form.title.data
        post_to_edit.subtitle = edit_blog_form.author.data
        post_to_edit.body = edit_blog_form.body.data
        post_to_edit.author = edit_blog_form.author.data
        post_to_edit.img_url = edit_blog_form.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', index=post_id))
    return render_template("make-post.html", form=edit_blog_form, id=post_id)


@app.route("/new-post", methods=["GET", "POST"])
def create_post():
    create_blog_post = CreatePostForm()
    if create_blog_post.validate_on_submit():
        now = datetime.now()
        blog_post = {field: value for field, value in create_blog_post.data.items() if field != 'submit' and field != 'csrf_token'}
        blog_post['date'] = now.strftime("%B %d, %Y")
        new_post = BlogPost(**blog_post)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=create_blog_post, to_edit=False)


@app.get("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
