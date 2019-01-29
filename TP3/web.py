from flask import Flask, render_template, url_for, request
from imdb import IMDb
from tf_idf import match


app = Flask(__name__)

IMDb_access = IMDb()

@app.route('/')
def search():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def getMovie():
    movie_name = request.form['movie_name']

    html_info = {}
    sugestions = []

    movies = IMDb_access.search_movie(movie_name)

    if movies != []:
        movie_infos = IMDb_access.get_movie(movies[0].getID())
        
        directors_names = []
        if 'directors' in movie_infos:
            directors = movie_infos['directors']
            directors_names = []
            for director in directors:
                directors_names.append(director['name'])

        html_info['Directors'] = ', '.join(directors_names)

        if 'languages' in movie_infos:
            html_info['Languages'] = ', '.join(movie_infos['languages'])

        if 'year' in movie_infos:
            html_info['Year'] = movie_infos['year']

        if 'kind' in movie_infos:
            html_info['Kind'] = movie_infos['kind']

        if 'rating' in movie_infos:
            html_info['Rating'] = movie_infos['rating']

        if 'genre' in movie_infos:
            html_info['Genre'] = ', '.join(movie_infos['genre'])

        sugestions = match(movie_infos['title'].lower())

        movie_name = []
        if 'title' in movie_infos:
            movie_name = movie_infos['title']

        cover_url = movie_infos['full-size cover url']
    else:
        movie_name = "Movie not available."
        cover_url = ""

    return render_template('movie.html', movie_name = movie_name, html_infos = html_info, cover_url = cover_url, sugestions = sugestions)

if __name__ == '__main__':
   app.run()