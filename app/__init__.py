from flask import Flask
from flask_login import LoginManager
from app.controller import CinemaController
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'somesecretkeythatonlyishouldknow'

# create a database object
db = SQLAlchemy()
# define a name for the database
DB_NAME = "database.db"

# Create an instance of CinemaController and load the database during application startup
LincolnCinema = CinemaController()
LincolnCinema.load_database()

from app.views import views

app.register_blueprint(views, url_prefix='/')

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     # Assuming 'user_id' is the customer's 'id' as in your 'Customer' class
#     customer = next((c for c in LincolnCinema.all_customers if c.id == int(user_id)), None)
#     return customer  # Return the customer object, or None if not found


if __name__ == "__main__":
    app.run(debug=True)