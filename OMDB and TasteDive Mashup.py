import requests_with_caching
import json

def get_movies_from_tastedive(input_title):
    base_url = 'https://tastedive.com/api/similar'
    param_d = {}
    param_d['q'] = input_title
    param_d['limit'] = 5
    param_d['type'] = 'movies'
    response = requests_with_caching.get(base_url, params = param_d)
    response_d=response.json()
    return response_d


def extract_movie_titles(dic):
    lst = []
    for item in dic['Similar']['Results']:
        lst.append(item['Name'])
    return(lst)


def get_related_titles(lst_movies):
    list = []
    for movie in lst_movies:
        new = extract_movie_titles(get_movies_from_tastedive(movie))
        for movie in new:
            if movie not in list:
                list.append(movie)
    return list


def get_movie_data(movie_title):
    base_url = "http://www.omdbapi.com/"
    d = {}
    d["t"] = movie_title
    d["r"] = "json"
    response = requests_with_caching.get(base_url,params = d)
    response_d = response.json()
    return response_d


def get_movie_rating(movieNameJson):
    strRanting=""
    for typeRantingList in movieNameJson["Ratings"]:
        if typeRantingList["Source"]== "Rotten Tomatoes":
            strRanting = typeRantingList["Value"]
    if strRanting != "":
        ranting = int(strRanting[:2])
    else: ranting = 0
    return ranting


def get_sorted_recommendations(listMovieTitle):
    listMovie= get_related_titles(listMovieTitle)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    
    return listMovie