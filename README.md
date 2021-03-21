# Movies API 
(Movie recommender included in the code, not in the deployment on heroku)

Movie recommender API done in Flask.

Deployed on heroku 
!!! The deployment works only as a demonstration of deployment of a Flask api, the free account cappacity doesn't allow the movie reccomender system to work and ends up in a app crash - if the app is crashed, please do let me know and I'll restart it.

 - to see all available movies (almost 10K): https://marketa-movies-app.herokuapp.com/api/v1/movies
 - to select movies from specific director (feel free to replace the name): https://marketa-movies-app.herokuapp.com/api/v1/directors?director=Tarantino
 - to select movies in which specific actor played (dtto): https://marketa-movies-app.herokuapp.com/api/v1/actors?actor=Smith
 - if you want to list movies with desired genre: https://marketa-movies-app.herokuapp.com/api/v1/genres?genre=Sci-Fi
 - if you want a brief description of a movie: https://marketa-movies-app.herokuapp.com/api/v1/description?title=Batman
 - or if you want to get a list of movies filtered by keyword in the description: https://marketa-movies-app.herokuapp.com/api/v1/filter_by_kw?keyword=horror

To see the code for these go through the app.py part: https://github.com/mvesela/imdb-movies-API/blob/main/app.py
To explore the more fancy/data sciency part - the movie recommender which works when you run the app locally see the movie_recommender.py (this is a basic implementation of a cosine similarity):  https://github.com/mvesela/imdb-movies-API/blob/main/movie_recommender.py

As a bonus for SW/Mandalorian fans I implemented custom 404: https://marketa-movies-app.herokuapp.com/api/v1/movie
