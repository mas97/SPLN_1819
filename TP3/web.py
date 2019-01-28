from flask import Flask, render_template, url_for, request
from imdb import IMDb



app = Flask(__name__)

IMDb_access = IMDb()

@app.route('/')
def search():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def getMovie():
    movie_name = request.form['movie_name']

    movies = IMDb_access.search_movie(movie_name)
    movie_infos = IMDb_access.get_movie(movies[0].getID())

    html_info = {}

    directors = movie_infos['directors']
    directors_names = []
    for director in directors:
        directors_names.append(director['name'])

    html_info['Directors'] = ', '.join(directors_names)

    html_info['Languages'] = ', '.join(movie_infos['languages'])

    html_info['Year'] = movie_infos['year']

    html_info['Kind'] = movie_infos['kind']

    html_info['Rating'] = movie_infos['rating']

    for key in movie_infos.keys():
        print(key)

    return render_template('movie.html', movie_name = movie_infos['title'], html_infos = html_info, cover_url = movie_infos['full-size cover url'])

if __name__ == '__main__':
   app.run()