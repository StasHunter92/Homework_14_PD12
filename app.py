from flask import Flask, jsonify
import utils

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/movie/<path:title>')
def movie_by_title(title: str):  # Return a movie by title
    result: dict | None = utils.get_movie_by_title(title)
    return jsonify(result)


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def movies_between_years(year_from: int, year_to: int):  # Return a list of movies between years
    result: list | None = utils.get_movies_between_years(year_from, year_to)
    return jsonify(result)


@app.route('/rating/<rating>')
def movies_by_rating(rating: str):  # Return a list of movies by rating
    result: list | None = utils.get_movies_by_rating(rating)
    return jsonify(result)


@app.route('/genre/<genre>')
def ten_last_films_by_genre(genre: str):  # Return ten last films by genre
    result: list | None = utils.get_ten_last_movies_by_genre(genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
