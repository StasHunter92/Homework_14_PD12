import sqlite3
from json import dumps
from sqlite3 import OperationalError


def get_result_from_database(query: str) -> list:
    """Main function to get the result from database"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result: list = connection.execute(query).fetchall()
        return result


def get_movie_by_title(title: str) -> dict | None:
    """Get a movie by title from the database"""
    query: str = f"""
            SELECT `title`, `country`, `release_year`, `listed_in` as genre, `description`
            FROM netflix
            WHERE `title` LIKE '%{title}%'
            ORDER BY `release_year` DESC
            LIMIT 1
            """
    result: list = get_result_from_database(query)
    for element in result:
        return dict(element)


def get_movies_between_years(year_from: int, year_to: int) -> list[dict] | None:
    """Get the list of 100 movies between two years"""
    query: str = f"""
            SELECT `title`, `release_year`
            FROM netflix
            WHERE `release_year` BETWEEN {year_from} AND {year_to}
            LIMIT 100
            """
    result: list = get_result_from_database(query)
    list_of_films: list = []
    for element in result:
        list_of_films.append(dict(element))
    if len(list_of_films) != 0:
        return list_of_films
    else:
        return None


def get_movies_by_rating(rating: str) -> list[dict] | None:
    """Get the list of movies by rating"""
    ratings_dict: dict = {
        "children": '("G")',
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    query: str = f"""
            SELECT `title`, `rating`, `description`
            FROM netflix
            WHERE `rating` IN {ratings_dict.get(rating)}
            """
    try:
        result: list = get_result_from_database(query)
        list_of_films: list = []
        for element in result:
            list_of_films.append(dict(element))
        if len(list_of_films) != 0:
            return list_of_films
        else:
            return None
    except OperationalError:
        return None


def get_ten_last_movies_by_genre(genre: str) -> list[dict] | None:
    """Get list of 10 movies by genre sorted by release year DESC"""
    query: str = f"""
            SELECT `title`, `description`
            FROM netflix
            WHERE `listed_in` LIKE '%{genre}%'
            ORDER BY `release_year` DESC
            LIMIT 10
            """
    result: list = get_result_from_database(query)
    list_of_films: list = []
    for element in result:
        list_of_films.append(dict(element))
    if len(list_of_films) != 0:
        return list_of_films
    else:
        return None


def get_movies_by_criteria(type_: str, year: int, genre: str) -> str:
    """Get a list of movies by criteria (type, year, genre)"""
    query: str = f"""
            SELECT `title`, `description`
            FROM netflix
            WHERE `type` = '{type_}' AND `release_year` = '{year}' AND `listed_in` LIKE '%{genre}%' 
            """
    result: list = get_result_from_database(query)
    list_of_films: list = []
    for element in result:
        list_of_films.append(dict(element))
    return dumps(list_of_films, ensure_ascii=False)


def get_actors_play_with(actor_1: str, actor_2: str) -> list[str] | list:
    """Returns a list of actors that have a play with the given actor"""
    query: str = f"""
            SELECT `cast`
            FROM netflix
            WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%'
            """
    result: list = get_result_from_database(query)
    actor_pair: list[str] = [actor_1, actor_2]
    actor_list: list = []
    for element in result:
        for actor in element[0].split(', '):
            if actor not in actor_pair:
                actor_list.append(actor)
    sorted_actor_list: list = []
    for actor in actor_list:
        if actor_list.count(actor) > 2:
            if actor not in sorted_actor_list:
                sorted_actor_list.append(actor)
    return sorted_actor_list
