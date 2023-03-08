from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__, instance_path="G:\Video Lectures\100DaysToCode\pythonProject\Library_SQLite")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///all-book-record.db"
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Books)).scalars()
    return render_template("index.html", book_list=list(all_books))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book = Books(
            title = request.form['name'],
            author = request.form['author'],
            rating = request.form['rating']
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get("id")
    book_to_edit_or_delete = db.get_or_404(Books, book_id)

    if bool(request.args.get('delete')):
        db.session.delete(book_to_edit_or_delete)
        db.session.commit()
        return redirect(url_for('home'))

    if request.method == "POST":
        book_to_edit_or_delete.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("change_rating.html", book=book_to_edit_or_delete)

if __name__ == "__main__":
    app.run(debug=True)
