from movies import *


def is_imdb_hight_enought(movie: dict) -> bool:
    return True if movie["imdb"] > 5.5 else False


def get_good_movies(movies: list) -> list:
    good_movies = []
    for movie in movies:
        if is_imdb_hight_enought(movie):
            good_movies.append(movie["name"])
    return good_movies


def get_category(category: str, movies: list) -> list:
    titles = []
    for movie in movies:
        if movie["category"] == category:
            titles.append(movie)
    return titles


def average_imdb(movies: list) -> float:
    return sum([movie["imdb"] for movie in movies]) / len(movies)


def average_category_imdb(category: str, movies: list) -> float:
    return average_imdb(get_category(category, movies))


print(is_imdb_hight_enought(movies[0]))
print(get_good_movies(movies))
print(get_category("Romance", movies))
print(average_imdb(movies))
print(average_category_imdb("War", movies))