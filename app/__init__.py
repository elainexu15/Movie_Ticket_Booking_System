from flask import Flask
from flask_login import LoginManager
from app.controller import CinemaController
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

UPLOAD_FOLDER = 'app/static/movie_img/'

bcrypt = Bcrypt(app)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create an instance of CinemaController and load the database during application startup
LincolnCinema = CinemaController()
LincolnCinema.load_database()
print(LincolnCinema.all_halls)
print(LincolnCinema.all_customers)

for movie in LincolnCinema.all_movies:
    for screening in movie.screenings:
        print(screening.is_active)

from app.views import views

app.register_blueprint(views, url_prefix='/')


if __name__ == "__main__":
    app.run(debug=True)