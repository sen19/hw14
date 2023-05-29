from flask import Flask
from config import Config
import logger as log
from dao.main_dao import MainDAO

app = Flask(__name__)
app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False


# Создаем DAO
main_dao = MainDAO("data/netflix.db")


def handle_bad_request(e):
    return f'bad request: {e}'


app.register_error_handler(404, handle_bad_request)
app.register_error_handler(500, handle_bad_request)


@app.route("/")
def page_index():
    return f"It works"


@app.route("/movie/<title>")
def page_movie_by_title(title):
    return main_dao.get_last_film_by_title(title)


@app.route("/movie/<first_year>/to/<last_year>")
def page_movies_by_years(first_year, last_year):
    return main_dao.get_films_by_years(first_year, last_year)


@app.route("/rating/children")
def page_movies_by_rating_children():
    return main_dao.get_films_by_rating(['G'])


@app.route("/rating/family")
def page_movies_by_rating_family():
    return main_dao.get_films_by_rating(['G', 'PG', 'PG-13'])


@app.route("/rating/adult")
def page_movies_by_rating_adult():
    return main_dao.get_films_by_rating(['R', 'NC-17'])


@app.route("/genre/<genre>")
def page_movies_by_genre(genre):
    return main_dao.get_last_film_by_genre(genre)


log.main_logger.info('App launched')
log.main_logger.info(main_dao.get_actors_by_actors('Rose McIver', 'Ben Lamb'))
log.main_logger.info(main_dao.get_actors_by_actors('Jack Black', 'Dustin Hoffman'))

if __name__ == "__main__":
    app.run(port=8000)
