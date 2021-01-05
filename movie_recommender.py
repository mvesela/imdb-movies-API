from flask import Blueprint
import pandas as pd
import sklearn.metrics.pairwise as pw
from scipy import sparse
from flask import request

movie_recommender = Blueprint('example_blueprint', __name__)


def clean_movies():
    movies = pd.read_csv('./movies.csv')
    ratings = pd.read_csv('./ratings.csv')
    # Extracting duplicated movie ids
    duplicate_movies = movies.groupby('title').filter(lambda x: len(x) == 2)
    duplic_ids = duplicate_movies['movieId'].values

    #Duplicated titles
    duplicate_movies = duplicate_movies[['movieId','title']]

    # Checking the id with most reviews
    review_count = pd.DataFrame(ratings[ratings['movieId'].isin(duplic_ids)]['movieId'].value_counts())
    review_count.reset_index(inplace=True)
    review_count.columns = ['movieId','count']
    duplicated_df = pd.merge(duplicate_movies, review_count, on='movieId')

    ## Getting duplicates with low review count
    duplicated_df.sort_values(by=['title', 'count'], ascending=[True,False])
    duplicated_ids = duplicated_df.drop_duplicates(subset="title", keep = 'last', inplace=False)['movieId']

    # Removing duplicated ids with low review count from movie database
    movies = movies.loc[~movies['movieId'].isin(duplicated_ids)]
    # Removing duplicated ids with low review count from rating database

    # creating list with unique genres
    genres = list(set('|'.join(list(movies["genres"].unique())).split('|')))
    genres.remove('(no genres listed)')

    # Creating dummy columns for each genre
    for genre in genres:
        movies[genre] = movies['genres'].map(lambda val: 1 if genre in val else 0)
    movies.drop('genres', axis=1, inplace=True)
    return movies


@movie_recommender.route("/api/v2/movies", methods=['GET'])
def get_movies():
    movies = clean_movies()
    movies['title'] = movies['title'].str.strip().str.replace(' ', '_').str.replace(',', '')
    movies['title'] = movies['title'].str.split("(", n=1, expand = True)
    movies['title'] = movies['title'].map(lambda x: str(x)[:-1])
    movies = movies[['title']].to_dict()
    return movies


def clean_ratings():
    movies = pd.read_csv('./movies.csv')
    ratings = pd.read_csv('./ratings.csv')
    # Extracting duplicated movie ids
    duplicate_movies = movies.groupby('title').filter(lambda x: len(x) == 2)
    duplic_ids = duplicate_movies['movieId'].values

    #Duplicated titles
    duplicate_movies = duplicate_movies[['movieId','title']]

    # Checking the id with most reviews
    review_count = pd.DataFrame(ratings[ratings['movieId'].isin(duplic_ids)]['movieId'].value_counts())
    review_count.reset_index(inplace=True)
    review_count.columns = ['movieId','count']
    duplicated_df = pd.merge(duplicate_movies, review_count, on='movieId')

    # Getting duplicates with low review count
    duplicated_df.sort_values(by=['title','count'],ascending=[True,False])
    duplicated_ids = duplicated_df.drop_duplicates(subset ="title", keep = 'last', inplace = False)['movieId']

    # Removing duplicated ids with low review count from movie database
    ratings = ratings.loc[~ratings['movieId'].isin(duplicated_ids)]
    # Removing duplicated ids with low review count from rating database
    ratings.drop('timestamp', axis=1, inplace=True)
    return ratings


def data():
    movies = clean_movies()
    ratings = clean_ratings()
    df = pd.merge(ratings, movies, on='movieId')
    return df


@movie_recommender.route("/api/v2/recommend_me_movie", methods=['GET'])
def item_based_recom():
    input_film_name = request.args.get('movie_i_like')
    input_dataframe = data()
    input_dataframe['title'] = input_dataframe['title'].str.strip().str.replace(' ', '_').str.replace(',', '')
    input_dataframe['title'] = input_dataframe['title'].str.split("(", n=1, expand=True)
    input_dataframe['title'] = input_dataframe['title'].map(lambda x: str(x)[:-1])
    pivot_item_based = pd.pivot_table(input_dataframe,
                                      index='title',
                                      columns=['userId'], values='rating')
    sparse_pivot = sparse.csr_matrix(pivot_item_based.fillna(0))
    recommender = pw.cosine_similarity(sparse_pivot)
    recommender_df = pd.DataFrame(recommender,
                                  columns=pivot_item_based.index,
                                  index=pivot_item_based.index)
    #recommender_df.to_pickle('./rec.gz', compression='gzip')
    cosine_df = pd.DataFrame(recommender_df[input_film_name].sort_values(ascending=False))
    cosine_df.reset_index(level=0, inplace=True)
    cosine_df.columns = ['title', 'cosine_sim']
    cosine_df['cosine_sim'] = cosine_df['cosine_sim'].round(2)*100
    cosine_df=cosine_df[1:10].to_dict()
    return cosine_df
