#!flask/bin/python
from flask import Flask
import pandas as pd
from flask import request
from flask import render_template
import os

from movie_recommender import movie_recommender

app = Flask(__name__)

app.register_blueprint(movie_recommender)


@app.route("/")
@app.route("/home")
def home():
    pics = os.listdir('static/images')
    return render_template("servebird.html", pics=pics)


@app.route("/api/v1/movies", methods=['GET'])
def get_all_movies():
    imdb = pd.read_csv('IMDB.csv')
    dict_of_movies = imdb['Title'].to_dict()
    return dict_of_movies


@app.route("/api/v1/actors", methods=['GET'])
def filter_by_actor():
    actor = request.args.get('actor')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Actors'].str.contains(actor)
    imdb = imdb.query("contains==True").reset_index()
    dict_of_movies = imdb['Title'].to_dict()
    return dict_of_movies


@app.route("/api/v1/directors", methods=['GET'])
def filter_by_director():
    director = request.args.get('director')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Director'].str.contains(director)
    imdb = imdb.query("contains==True").reset_index()
    dict_of_movies = imdb['Title'].to_dict()
    return dict_of_movies


@app.route("/api/v1/genres", methods=['GET'])
def filter_by_genre():
    genre = request.args.get('genre')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Genre'].str.contains(genre)
    imdb = imdb.query("contains==True").reset_index()
    dict_of_movies = imdb['Title'].to_dict()
    return dict_of_movies


@app.route("/api/v1/ratings", methods=['GET'])
def get_movie_rating():
    title = request.args.get('title')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Title'].str.contains(title)
    imdb = imdb.query("contains==True").reset_index()
    rating = imdb['Rating'].to_dict()
    return rating[0]


@app.route("/api/v1/description", methods=['GET'])
def get_movie_description():
    title = request.args.get('title')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Title'].str.contains(title)
    imdb = imdb.query("contains==True").reset_index()
    desc = imdb['Description'].to_dict()
    return desc[0]


@app.route("/api/v1/filter_by_kw", methods=['GET'])
def filter_by_keyword():
    keyword = request.args.get('keyword')
    imdb = pd.read_csv('IMDB.csv')
    imdb['contains'] = imdb['Description'].str.contains(keyword)
    imdb = imdb.query("contains==True").reset_index()
    titles = imdb['Title'].to_dict()
    return titles


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
