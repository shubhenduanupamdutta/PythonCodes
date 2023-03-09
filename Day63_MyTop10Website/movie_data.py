import requests
from database_classes import Movie

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NDFiZDg3YTYxMDdjNzcxNDBjYzJiZjZjN2U0ZjQyMyIsInN1YiI6IjY0MDlhNTNmNzc3NmYwMDA4YzJmNjYzYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kKALoQIbqL-fjrYAgBO3RlDOZ4HxxpV05ekfSvrNKc8"
}

endpoint_poster = "https://www.themoviedb.org/t/p/original"

endpoint = "https://api.themoviedb.org/3/search/movie"


def get_movie_data(title: str) -> list:
    parameters = {
        "query": title,
    }
    response = requests.get(url=endpoint, headers=headers, params=parameters)
    data = response.json()
    print(data)
    return data['results']



def movie_details_by_id(movie_id: str) -> Movie:
    url = "https://api.themoviedb.org/3/movie/" + movie_id
    response = requests.get(url=url, headers=headers)
    movie_data = response.json()
    movie = Movie()
    movie.title = movie_data['original_title']
    movie.year = movie_data['release_date'].split("-")[0]
    movie.description = movie_data['overview']
    movie.rating = round(float(movie_data['vote_average']),1)
    movie.image_url = endpoint_poster + movie_data['poster_path']
    return movie


# movie_details_by_id(161)