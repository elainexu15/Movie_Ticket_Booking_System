from flask import Blueprint, flash
from . import LincolnCinema
from .models import *
from flask import g, redirect, render_template, request, session, url_for, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import urllib.request
from app import app
from werkzeug.utils import secure_filename
import json


views = Blueprint('views', __name__)

LANGUAGE_LIST = sorted(LincolnCinema.get_language_list())
GENRE_LIST = sorted(LincolnCinema.get_genre_list())
ALLOWED_EXTENSIONS = set(['jpg'])


# ======== admin functions ========
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import request, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import os


# ========= Admin views =========
@views.route('/admin_add_movie', methods=['POST', 'GET'])
def admin_add_movie():
    if request.method == 'POST':

        # Get movie information from the form
        title = request.form.get('title')
        genre = request.form.get('genre')
        release_date = request.form.get('release_date')
        country = request.form.get('country')
        duration = request.form.get('duration')
        language = request.form.get('language')
        description = request.form.get('description')

        # Create a Movie object
        movie = Movie(title, language, genre, country, release_date, duration, description)
        LincolnCinema.add_movie(movie)
        
         # Load existing movie data from movies.json if it exists
        movie_data = []
        try:
            with open('movies.json', 'r') as json_file:
                movie_data = json.load(json_file)
        except FileNotFoundError:
            pass

        # Append the new movie data to the existing data
        movie_data.append({
            "title": title,
            "language": language,
            "genre": genre,
            "country": country,
            "release_date": release_date,
            "duration": duration,
            "description": description,
            "screenings": []
        })

        # Save the updated movie data back to movies.json
        with open('app/database/movies.json', 'w') as json_file:
            json.dump(movie_data, json_file, indent=4)

        flash('Movie information has been saved.')

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(movie.id) + os.path.splitext(file.filename)[1])            
            destination_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(destination_folder, exist_ok=True)  # Create the folder if it doesn't exist
            file.save(os.path.join(destination_folder, filename))
            flash('Image successfully uploaded and displayed below')
            return render_template('movie_details.html', movie=movie, filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('admin_add_movie.html')


@views.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='movie_img/' + filename), code=301)


@views.route('/admin_view_movie_details/<movie_id>')
def admin_view_movie_details(movie_id):
    movie_id = int(movie_id)
    movie = LincolnCinema.find_movie(movie_id)
    screening_date_list = movie.get_screening_date_list()
    return render_template('admin_view_movie_details.html', movie = movie, screening_date_list=screening_date_list)


@views.route('/admin_cancel_movie/<int:movie_id>', methods=['GET', 'POST'])
def admin_cancel_movie(movie_id):

    return redirect(url_for("views.admin_home"))

@views.route('/admin_add_screening/<int:movie_id>', methods=['GET', 'POST'])
def admin_add_screening(movie_id):
    # Get the movie based on its ID
    movie = LincolnCinema.find_movie(movie_id)
    hall_name_list = [hall.hall_name for hall in LincolnCinema.all_halls]
    
    if request.method == 'POST':
        screening_date = request.form['screening_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        hall_name = request.form['hall_name']
        price = request.form['price']

        # convert time to 24-hour format
        start_time = datetime.strptime(start_time, '%H:%M').strftime('%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M').strftime('%H:%M')        
        
        # Calculate the ending time based on start_time and movie.duration_in_minutes
        movie_duration_in_mins = int(movie.duration_in_mins) 

        start_datetime = datetime.strptime(start_time, '%H:%M')
        calculated_end_time = start_datetime + timedelta(minutes=movie_duration_in_mins)
        selected_end_datetime = datetime.strptime(end_time, '%H:%M')

        if selected_end_datetime <= calculated_end_time:
            flash('Invalid end time. Show time should be no shorter than Movie duration.', 'error')
            return render_template('admin_add_screening.html', movie=movie, hall_name_list=hall_name_list)
        
        # get hall object
        hall = LincolnCinema.find_hall(hall_name)
        
        seats = LincolnCinema.initialise_seats(hall, price)
        # Create a CinemaScreening object
        screening = Screening(screening_date, start_time, end_time, hall, seats)

        # Add the screening to the movie
        movie.add_screening(screening)

        # Get the seat data for this screening
        seats = [seat.to_json() for seat in screening.seats]

        screening_data = {
        "screening_date": screening_date,
        "start_time": start_time,
        "end_time": end_time,
        "hall_name": hall_name,
        "price": price,
        "seats": seats
    }

        # Define the filename based on the movie ID
        filename = f'app/database/screenings_{movie_id}.json'

        if os.path.exists(filename):
            # File exists, so let's read the existing data
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            # File doesn't exist, create an empty list
            existing_data = []

        # Append the new screening data to the existing data
        existing_data.append(screening_data)

        # Write the updated data back to the file
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        flash('Screening has been added.')

        screening_date_list = movie.get_screening_date_list()

        return render_template('admin_view_movie_details.html', movie = movie, screening_date_list=screening_date_list)
    return render_template('admin_add_screening.html', movie=movie, hall_name_list=hall_name_list)



@views.route('/')
def home():
    return render_template('home.html')


@views.before_request
def before_request():
    g.user = None

    if 'user_username' in session:
        user = next((x for x in LincolnCinema.all_customers if x.username == session['user_username']), None)
        if user is None:
            user = next((x for x in LincolnCinema.all_admins if x.username == session['user_username']), None)
        if user is None:
            user = next((x for x in LincolnCinema.all_front_desk_staffs if x.username == session['user_username']), None)
        if user:
            g.user = user



@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_username', None)

        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("Both username and password are required.", 'error')
            return redirect(url_for('views.login'))

        user = None
        try:
            user = next((x for x in LincolnCinema.all_customers if x.username == username), None)
            if user is None:
                user = next((x for x in LincolnCinema.all_admins if x.username == username), None)
            if user is None:
                user = next((x for x in LincolnCinema.all_front_desk_staffs if x.username == username), None)
        except StopIteration:
            user = None

        if user is not None and check_password_hash(user.password, password):
            session['user_username'] = user.username
            if isinstance(user, Customer):
                flash("Login successful!", 'success')
                return redirect(url_for('views.customer_home'))
            elif isinstance(user, Admin):
                flash("Login successful!", 'success')
                return redirect(url_for('views.admin_home'))
            elif isinstance(user, FrontDeskStaff):
                flash("Login successful!", 'success')
                return redirect(url_for('views.home_front_desk_staff'))
        else:
            flash("Invalid username or password. Please try again.", 'error')
            return redirect(url_for('views.login'))

    return render_template('login.html')




@views.route('/admin_home')
def admin_home():
    if not g.user:
        return redirect(url_for('views.login'))
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('admin_home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list)


@views.route('/home_front_desk_staff')
def home_front_desk_staff():
    if not g.user:
        return redirect(url_for('views.login'))
    return render_template('home_front_desk_staff.html')


@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if LincolnCinema.find_customer(username):
            flash("Username already exists. Please choose a different one.", category='error')
            return redirect(url_for('views.register'))
        
        hashed_password = generate_password_hash(password, method='sha256')

        registration_result = LincolnCinema.register_customer(name, address, email, phone, username, hashed_password)
   

        if registration_result:
            flash("Registration successful. You can now log in.", category='success')
            return redirect(url_for('views.login'))
        else:
            flash("Registration failed. Please try again.", category='error')
            return redirect(url_for('views.register'))

    return render_template('register.html')


@views.route('/logout')
def logout():
    if 'user_username' in session:
        session.pop('user_username', None)
    return redirect(url_for('views.home'))

@views.route('/all_movies')
def all_movies():
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('movies.html', all_movies = all_movies, language_list = language_list, 
                           genre_list = genre_list)


@views.route('/filter_movies', methods=['GET', 'POST'])
def filter_movies():
    if request.method == 'POST':
        # Get the customer's selected filters from the form
        title = request.form.get('title')
        selected_language = request.form.get('language')
        selected_genre = request.form.get('genre')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        if date_from and not date_to:
            date_to = str(date.today())
        elif date_to and not date_from:
            date_from = '1900-01-01'
        guest = Guest()
        
        # filter movies 
        filtered_movies = LincolnCinema.filter_movies(title, selected_language, selected_genre, date_from, date_to, guest)
        
        language_list = LANGUAGE_LIST
        genre_list = GENRE_LIST
        return render_template('admin_home.html', all_movies=filtered_movies, language_list = language_list, 
                           genre_list = genre_list)

    # If the method is GET, initially display the form
    return redirect(url_for('views.all_movies'))

# ======= CUSTOMER VIEWS =======
@views.route('/customer_home')
def customer_home():
    if not g.user:
        return redirect(url_for('views.login'))
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('cus_home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list)


@views.route('/customer_view_movie_details/<movie_id>')
def customer_view_movie_details(movie_id):
    movie_id = int(movie_id)
    movie = LincolnCinema.find_movie(movie_id)
    screening_date_list = movie.get_screening_date_list()
    return render_template('cus_view_movie_details.html', movie = movie, screening_date_list=screening_date_list)


@views.route('/customer_filter_movies/<customer_username>', methods=['GET', 'POST'])
def customer_filter_movies(customer_username):
    print(customer_username)
    customer = LincolnCinema.find_customer(customer_username)
    if request.method == 'POST':
        # Get the customer's selected filters from the form
        title = request.form.get('title')
        selected_language = request.form.get('language')
        selected_genre = request.form.get('genre')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        if date_from and not date_to:
            date_to = str(date.today())
        elif date_to and not date_from:
            date_from = '1900-01-01'

        # filter movies 
        filtered_movies = LincolnCinema.customer_filter_movies(title, selected_language, selected_genre, date_from, date_to, customer)
        language_list = LANGUAGE_LIST
        genre_list = GENRE_LIST
        return render_template('cus_home.html', all_movies=filtered_movies, language_list = language_list, 
                           genre_list = genre_list)

    # If the method is GET, initially display the form
    return redirect(url_for('views.customer_home'))