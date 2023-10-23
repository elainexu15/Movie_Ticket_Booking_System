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

# create a database object
db = SQLAlchemy()
# define a name for the database
DB_NAME = "database.db"

# Create an instance of CinemaController and load the database during application startup
LincolnCinema = CinemaController()
LincolnCinema.load_database()
print(LincolnCinema.all_admins)
print(LincolnCinema.all_front_desk_staffs)
# for hall in LincolnCinema.all_halls:
#     for seat in hall.seats:
#         print(seat)

from app.views import views

app.register_blueprint(views, url_prefix='/')


if __name__ == "__main__":
    app.run(debug=True)