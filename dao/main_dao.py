from flask import jsonify
import sqlite3


class MainDAO:

    def __init__(self, path):
        self.path = path

    def _load(self, query):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
        return cursor.fetchall()

    def get_last_film_by_title(self, title):
        """возвращает сведения о фильме по его названию"""
        query = f"""SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE \"%{title}%\"
                    ORDER BY release_year DESC
                    LIMIT 1
                """
        rows = self._load(query)
        try:
            film_data = {"title": rows[0][0],
                         "country": rows[0][1],
                         "release_year": rows[0][2],
                         "genre": rows[0][3],
                         "description": rows[0][4]
                         }
        except IndexError:
            return 'Не найдено'
        return film_data

    def get_films_by_years(self, first_year, last_year):
        """возвращает фильмы по годам"""
        query = f"""SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN \"{first_year}\" and \"{last_year}\"
                    ORDER BY release_year DESC
                    LIMIT 100
                """
        rows = self._load(query)
        film_data = []
        try:
            for row in rows:
                film_data.append({"title": row[0],
                                  "release_year": row[1]
                                  })
        except IndexError:
            return 'Не найдено'
        return jsonify(film_data)

    def get_films_by_rating(self, ratings: list):
        """возвращает фильмы по рейтингам"""
        film_data = []
        for rating in ratings:
            query = f"""SELECT title, rating, description
                        FROM netflix
                        WHERE rating = \"{rating}\"
                        ORDER BY release_year DESC
                        LIMIT 100
                    """
            rows = self._load(query)
            try:
                for row in rows:
                    film_data.append({"title": row[0],
                                      "rating": row[1],
                                      "description": row[2]
                                      })
            except IndexError:
                return 'Не найдено'
        return jsonify(film_data)

    def get_last_film_by_genre(self, genre):
        """возвращает сведения о фильме по его жанру"""
        query = f"""SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE \"%{genre}%\"
                    ORDER BY release_year DESC
                    LIMIT 10
                """
        rows = self._load(query)
        film_data = []
        try:
            for row in rows:
                film_data.append({"title": row[0],
                                  "description": row[1]
                                  })
        except IndexError:
            return 'Не найдено'
        return jsonify(film_data)

    def get_actors_by_actors(self, actor1, actor2):
        """возвращает сведения о партнерах двух актеров"""
        query = f"""SELECT `cast`
                    FROM netflix
                    WHERE `cast` LIKE \"%{actor1}%{actor2}%\" OR \"%{actor2}%{actor1}%\"
                """
        rows = self._load(query)
        actors = []
        actors_union = []
        selected_actors = []
        for row in rows:
            actors.append(row[0].split(', '))
        for actor in actors:
            actors_union.extend(actor)
        for actor in actors_union:
            if actor not in selected_actors and actors_union.count(actor) > 2 and actor != actor1 and actor != actor2:
                selected_actors.append(actor)
        return selected_actors

    def get_films(self, user_type, user_year, genre):
        """возвращает сведения о фильмах по запросу из типа, жанра и года"""
        query = f"""SELECT title, description
                    FROM netflix
                    WHERE (`type` LIKE \"%{user_type}%\") AND (release_year = \"{user_year}\") AND (listed_in LIKE \"%{genre}%\")
                """
        rows = self._load(query)
        return jsonify(rows)
