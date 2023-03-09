from flask import Flask, render_template, url_for, request, redirect, flash
from pathlib import Path
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_forms import *
from database_tables import *
from sqlalchemy.exc import IntegrityError

# Initializing parameters, apps
cur_dir = Path()
database_dir = cur_dir / 'databases'
app = Flask(__name__, instance_path=database_dir.resolve())
app.secret_key = "alsdkfja90adfa4s6df7asdf32a1sdf"
bootstrap = Bootstrap5(app)

# Initializing Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library-record.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():  # put application's code here
    all_books = db.session.execute(db.select(BookList)).scalars()
    return render_template('index.html', books=list(all_books))


@app.route('/add', methods=["GET", "POST"])
def add_book():
    form_add_book = AddBook()
    if form_add_book.validate_on_submit():
        new_book = BookList(
            title=form_add_book.title.data,
            author=form_add_book.author.data,
            rating=form_add_book.rating.data
        )
        db.session.add(new_book)
        try:
            db.session.commit()
        except IntegrityError:
            flash("IntegrityError: This book is already in the database.", category="IntegrityError")
            return render_template("add_book.html", form=form_add_book)

        return redirect(url_for('home'))
    return render_template("add_book.html", form=form_add_book)


@app.context_processor
def inject_variables():
    cur_year = datetime.now().year
    return dict(year=cur_year)


@app.get("/delete")
def delete_book():
    id = request.args.get("book_id", type=int)
    book = db.get_or_404(BookList, id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit', methods=["GET", "POST"])
def edit_rating():
    id = request.args.get("book_id", type=int)
    book = db.get_or_404(BookList, id)
    edit_form = EditBook()
    if edit_form.validate_on_submit():
        book.rating = edit_form.new_rating.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form, book=book)


if __name__ == "__main__":
    app.run()
