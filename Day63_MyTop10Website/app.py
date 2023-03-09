from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from database_classes import *
from flask_forms import *
from pathlib import Path
from movie_data import *
from datetime import datetime

# Initializing Flask and Bootstrap
cur_directory = Path("G:/Video Lectures/100DaysToCode/pythonProject/Movie_List_DB_Flask_WTF_BS") / 'databases'
app = Flask(__name__, instance_path=cur_directory.resolve())
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

# Initializing Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-favourite-movies.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    # movie = Movie(
    #     title="Ocean Eleven",
    #     year=2001,
    #     description="Danny Ocean and his ten accomplices plan to rob three Las Vegas casinos simultaneously.",
    #     rating=7.7,
    #     ranking=5,
    #     review="Great Entertainment.",
    #     image_url="https://images.justwatch.com/poster/285528470/s718/oceans-eleven.%7Bformat%7D"
    # )
    # db.session.add(movie)
    # db.session.commit()


def rank_movies(movies: list[Movie]):
    for idx, movie in enumerate(movies):
        movie.ranking = idx + 1
    db.session.commit()


@app.route("/")
def home():
    movie_list = list(db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars())
    rank_movies(movie_list)
    return render_template("index.html", movies=movie_list)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    edit_form = RateMovieForm()
    id = request.args.get("movie_id")
    movie = db.get_or_404(Movie, id)
    if edit_form.validate_on_submit():
        movie.rating = edit_form.rating.data
        movie.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form, movie=movie)


@app.get("/delete")
def delete_movie():
    id = request.args.get("movie_id")
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    # movie_list = list(db.session.execute(db.select(Movie).filter(Movie.c.ranking > movie.ranking)).scalars())
    # for movie in movie_list:
    #     movie.ranking = movie.ranking - 1;
    # .c represents column selection
    table = Movie.__table__
    db.session.execute(table.update().where(table.c.ranking > movie.ranking).values(ranking=table.c.ranking - 1))
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_movie_form = AddMovie()
    if add_movie_form.validate_on_submit():
        movie_title = add_movie_form.movie_name.data
        movie_list = get_movie_data(movie_title)
        return render_template("select.html", movies=movie_list)
    if request.args.get("id"):
        mdb_id = request.args.get('id')
        get_movie = movie_details_by_id(mdb_id)
        get_movie.id = int(mdb_id)
        db.session.add(get_movie)
        db.session.commit()
        return redirect(url_for('edit_movie', movie_id=get_movie.id))
    return render_template('add.html', form=add_movie_form)


@app.context_processor
def inject_year():
    cur_year = datetime.now().year
    return dict(year=cur_year)


if __name__ == '__main__':
    app.run(debug=True)
