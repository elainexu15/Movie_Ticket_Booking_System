from flask import Blueprint, flash
from . import LincolnCinema
from .models import *
from flask import g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import requests


views = Blueprint('views', __name__)

@views.route('/index')
def index():
    raw_data = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=b5a0eeb8&s=batman')
    movies = raw_data.json()
    return render_template('index.html', movies = movies)

@views.route('/')
def home():
    print(LincolnCinema.all_customers)
    return render_template('home.html')


@views.before_request
def before_request():
    g.user = None

    if 'user_username' in session:
        user = next((x for x in LincolnCinema.all_customers if x.username == session['user_username']), None)
        if user:
            g.user = user


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
            print(user.name)
            print(user.username)



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
            print(user.username)
            if isinstance(user, Customer):
                flash("Login successful!", 'success')
                return redirect(url_for('views.customer_dashboard'))
            elif isinstance(user, Admin):
                flash("Login successful!", 'success')
                return redirect(url_for('views.admin_dashboard'))
            elif isinstance(user, FrontDeskStaff):
                flash("Login successful!", 'success')
                return redirect(url_for('views.staff_dashboard'))
        else:
            flash("Invalid username or password. Please try again.", 'error')
            return redirect(url_for('views.login'))

    return render_template('login.html')


@views.route('/customer_dashboard')
def customer_dashboard():
    if not g.user:
        return redirect(url_for('views.login'))
    return render_template('customer_dashboard.html')


@views.route('/admin_dashboard')
def admin_dashboard():
    if not g.user:
        return redirect(url_for('views.login'))
    return render_template('admin_dashboard.html')


@views.route('/staff_dashboard')
def staff_dashboard():
    if not g.user:
        return redirect(url_for('views.login'))
    return render_template('staff_dashboard.html')


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
            print("Username already exists. Please choose a different one.")
            flash("Username already exists. Please choose a different one.", category='error')
            print(LincolnCinema.all_customers)
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
    current_year = datetime.datetime.now().year
    all_movies = LincolnCinema.all_movies
    language_list = LincolnCinema.get_language_list()
    genre_list = LincolnCinema.get_genre_list()
    release_year_list = [i for i in range(current_year,current_year - 13, -1)]
    return render_template('all_movies.html', all_movies = all_movies, language_list = language_list, 
                           genre_list = genre_list, release_year_list = release_year_list, current_year = current_year)


@views.route('/search_by_title', methods = ['POST'])
def search_by_title():
    if request.method == 'POST':
        title = request.form.get('title')
        print(title)
    return redirect(url_for('views.all_movies'))


@views.route('/filter_movies', methods=['GET', 'POST'])
def filter_movies():
    if request.method == 'POST':
        # Get the customer's selected filters from the form
        selected_language = request.form.get('language')
        selected_genre = request.form.get('genre')
        selected_year = request.form.get('year')
        print(selected_year)
        guest = Guest()

        filtered_movies = LincolnCinema.filter_movies(selected_language, selected_genre, selected_year, guest)

        current_year = datetime.datetime.now().year
        language_list = LincolnCinema.get_language_list()
        genre_list = LincolnCinema.get_genre_list()
        release_year_list = [i for i in range(current_year,current_year - 13, -1)]
        return render_template('all_movies.html', all_movies=filtered_movies, language_list = language_list, 
                           genre_list = genre_list, release_year_list = release_year_list, current_year = current_year)

    # If the method is GET, initially display the form
    return render_template('your_original_template.html')