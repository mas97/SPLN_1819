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

    movies = IMDb_access.search_movie(movie_name)

    if movies != []:
        movie_infos = IMDb_access.get_movie(movies[0].getID())
        print(movie_infos)
        
        directors_names = []
        try:
            directors = movie_infos['directors']
            for director in directors:
                directors_names.append(director['name'])
        except:
            directors_names = []

        html_info['Directors'] = ', '.join(directors_names)

        try:
            html_info['Languages'] = ', '.join(movie_infos['languages'])
        except:
            html_info['Languages'] = ''

        try:
            html_info['Year'] = movie_infos['year']
        except:
            html_info['Year'] = ''

        try:
            html_info['Kind'] = movie_infos['kind']
        except:
            html_info['Kind'] = ''

        try:
            html_info['Rating'] = movie_infos['rating']
        except:
            html_info['Rating'] = ''

        try:
            html_info['Genres'] = ', '.join(movie_infos['genres'])
        except:
            html_info['Genres'] = ''

        try:
             movie_name = movie_infos['title']
        except:
            movie_name = 'Movie not Available'

        try:
            cover_url = movie_infos['full-size cover url']
        except:
            cover_url = ''
        
        try:
            movie_title = movie_infos['title'].replace(":","")
            suggestions = match(movie_title.lower())
            suggestion_error = False
        except:
            suggestion_error = True

    return render_template('movie.html', movie_name = movie_name, html_infos = html_info, cover_url = cover_url, suggestions = suggestions, suggestion_error = suggestion_error)

if __name__ == '__main__':
   app.run()