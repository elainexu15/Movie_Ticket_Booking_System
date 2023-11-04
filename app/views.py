# Import required libraries
from flask import Blueprint, flash
from . import LincolnCinema
from .models import *
from flask import g, redirect, render_template, request, session, url_for, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from app import app
from werkzeug.utils import secure_filename
import json


# Create a Blueprint named 'views'
views = Blueprint('views', __name__)


# CONSTANT VARIABLES
LANGUAGE_LIST = sorted(LincolnCinema.get_language_list())
GENRE_LIST = sorted(LincolnCinema.get_genre_list())
ALLOWED_EXTENSIONS = set(['jpg'])


# Define a function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ========= Authentication Routes =========
# Route for the home page
@views.route('/')
def home():
    # Retrieve a list of all movies, language list, and genre list
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list )


# Define a function to be executed before each request
@views.before_request
def before_request():
    g.user = None

    if 'user_username' in session:
        # Try to find the user in customers, admins, and front_desk_staffs
        user = next((x for x in LincolnCinema.all_customers if x.username == session['user_username']), None)
        if user is None:
            user = next((x for x in LincolnCinema.all_admins if x.username == session['user_username']), None)
        if user is None:
            user = next((x for x in LincolnCinema.all_front_desk_staffs if x.username == session['user_username']), None)
        if user:
            g.user = user


# Route for the login page
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_username', None)
        # Retrieve the submitted username and password
        username = request.form['username']
        password = request.form['password']
        
        # Check if both username and password are provided
        if not username or not password:
            flash("Both username and password are required.", 'error')
            return redirect(url_for('views.login'))

        user = None
        try:
            # Try to find the user in customers, admins, and front_desk_staffs
            user = next((x for x in LincolnCinema.all_customers if x.username == username), None)
            if user is None:
                user = next((x for x in LincolnCinema.all_admins if x.username == username), None)
            if user is None:
                user = next((x for x in LincolnCinema.all_front_desk_staffs if x.username == username), None)
        except StopIteration:
            user = None
        #  Validate user credentials
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
                return redirect(url_for('views.staff_home'))
        else:
            flash("Invalid username or password. Please try again.", 'error')
            return redirect(url_for('views.login'))

    return render_template('login.html')


# Define a route for the registration page
@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user registration information from the form
        name = request.form['name'].title()
        address = request.form['address'].title()
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']  # Added password_repeat
        
        # Check if the username already exists
        if LincolnCinema.check_duplicate_username(username) == True:
            flash("Username already exists. Please choose a different one.", category='error')
            return redirect(url_for('views.register'))
        
        # Check if the email already exists
        if LincolnCinema.check_duplicate_email(email) == True:
            flash("This email has already registered.", category='error')
            return redirect(url_for('views.register'))
        
        # Check if the passwords match
        if password != password_repeat:
            flash("Passwords do not match. Please try again.", category='error')
            return redirect(url_for('views.register'))
        
        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')
        # Split the name into words and capitalize the first letter of each word
        name = ' '.join(word.capitalize() for word in name.split())
        # Attempt to register the user
        registration_result = LincolnCinema.register_customer(name, address, email, phone, username, hashed_password)
   
        if registration_result:
            print(f'new customer{registration_result}')
            flash("Registration successful. You can now log in.", category='success')
            return redirect(url_for('views.login'))
        else:
            flash("Registration failed. Please try again.", category='error')
            return redirect(url_for('views.register'))

    return render_template('register.html')


# Route for logging out
@views.route('/logout')
def logout():
     # Remove the user's username from the session
    if 'user_username' in session:
        session.pop('user_username', None)
    return redirect(url_for('views.home'))



# ======== View movie details ========
# Route to view movie details for admin
@views.route('/view_movie_details/<movie_id>')
def view_movie_details(movie_id):
    # check if user logged in and find is user a customer, admin or staff
    if g.user:
        username = g.user.username
        customer = LincolnCinema.find_customer(username)
        admin = LincolnCinema.find_admin(username)
        staff = LincolnCinema.find_staff(username)

        if customer:
            user = customer
        elif admin:
            user = admin
        elif staff:
            user = staff
    else:
        # Create a Guest object
        user = Guest()

    # get movie ID
    movie_id = int(movie_id)
    # find movie object
    movie = LincolnCinema.find_movie(movie_id)
    # Filter the list of screenings to include only active screenings
    active_screenings = [screening for screening in movie.screenings if screening.is_active == True]
    # Get a list of screening dates for the movie
    screening_date_list = movie.get_screening_date_list()

    if isinstance(user, Customer):
        # Customer
        return render_template('cus_view_movie_details.html', movie=movie, screening_date_list=screening_date_list, active_screenings=active_screenings)
    elif isinstance(user, FrontDeskStaff):
        # Front Desk Staff
        return render_template('staff_view_movie_details.html', movie=movie, screening_date_list=screening_date_list, active_screenings=active_screenings)
    elif isinstance(user, Admin):
        # Admin
        return render_template('admin_view_movie_details.html', movie=movie, screening_date_list=screening_date_list, active_screenings=active_screenings)
    elif isinstance(user, Guest):
        # Admin
        return render_template('guest_view_movie_details.html', movie=movie, screening_date_list=screening_date_list, active_screenings=active_screenings)



# ============ Filter Movies ============
# Route for filtering movies based on customer preferences
@views.route('/filter_movies', methods=['GET', 'POST'])
def filter_movies():
    # check if user logged in and find is user a customer, admin or staff
    if g.user:
        username = g.user.username
        customer = LincolnCinema.find_customer(username)
        admin = LincolnCinema.find_admin(username)
        staff = LincolnCinema.find_staff(username)

        if customer:
            user = customer
        elif admin:
            user = admin
        elif staff:
            user = staff
    else:
        # Create a Guest object
        user = Guest()

    if request.method == 'POST':
        # Get the customer's selected filters from the form
        title = request.form.get('title')
        selected_language = request.form.get('language')
        selected_genre = request.form.get('genre')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')

        # Handle date filtering
        if date_from and not date_to:
            date_to = str(date.today())
        elif date_to and not date_from:
            date_from = '1900-01-01'

        # Filter movies based on the selected criteria
        filtered_movies = LincolnCinema.filter_movies(title, selected_language, selected_genre, date_from, date_to, user)
        language_list = LANGUAGE_LIST
        genre_list = GENRE_LIST

        if isinstance(user, Customer):
            # Customer
            return render_template('cus_home.html', all_movies=filtered_movies, language_list=language_list, genre_list=genre_list)
        elif isinstance(user, FrontDeskStaff):
            # Front Desk Staff
            return render_template('staff_home.html', all_movies=filtered_movies, language_list=language_list, genre_list=genre_list)
        elif isinstance(user, Admin):
            # Admin
            return render_template('admin_home.html', all_movies=filtered_movies, language_list=language_list, genre_list=genre_list)
        elif isinstance(user, Guest):
            # Admin
            return render_template('home.html', all_movies=filtered_movies, language_list=language_list, genre_list=genre_list)

    # If the method is GET, initially display the form
    if isinstance(user, Customer):
        # Customer
        return redirect(url_for('views.customer_home'))
    elif isinstance(user, FrontDeskStaff):
        # Front Desk Staff
        return redirect(url_for('views.staff_home'))
    elif isinstance(user, Admin):
        # Admin
        return redirect(url_for('views.admin_home'))
    elif isinstance(user, Guest):
        # Guest
        return redirect(url_for('views.home'))



# ========= Admin Routes =========
# route for the admin home page
@views.route('/admin_home')
def admin_home():
    # Check if there is an authenticated user, otherwise redirect to the login page
    if not g.user:
        return redirect(url_for('views.login'))
    # Retrieve a list of all movies, language list, and genre list
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('admin_home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list)

# route for adding a new movie by admin
@views.route('/admin_add_movie', methods=['POST', 'GET'])
def admin_add_movie():
    if request.method == 'POST':
        # Get movie information from the form
        title = request.form.get('title').upper()
        genre = request.form.get('genre').title()
        release_date = request.form.get('release_date')
        country = request.form.get('country').title()
        duration = request.form.get('duration')
        language = request.form.get('language').title()
        description = request.form.get('description').title()
        
        # Check if a file is provided in the form
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading', 'error')
            return redirect(request.url)
        
        # Check if the file is an allowed image format
        if file and allowed_file(file.filename):
            # Create a Movie object
            movie = Movie(title, language, genre, country, release_date, duration, description)
            LincolnCinema.add_movie(movie)
            Movie.save_new_movie_to_file(movie)

            # Generate a unique filename and save the image to a destination folder
            filename = secure_filename(str(movie.id) + os.path.splitext(file.filename)[1])            
            destination_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(destination_folder, exist_ok=True)  # Create the folder if it doesn't exist
            file.save(os.path.join(destination_folder, filename))
            flash('Image successfully uploaded and displayed below')
            # Redirect to the movie details page
            return render_template('admin_view_movie_details.html', movie=movie, filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif. Please try again.', 'error')
            return redirect(request.url)
    return render_template('admin_add_movie.html')


# Route to display an image by filename
@views.route('/display/<filename>')
def display_image(filename):
    # Redirect to the static folder to display an image
    return redirect(url_for('static', filename='movie_img/' + filename), code=301)


# Route to cancel a movie by admin
@views.route('/admin_cancel_movie/<int:movie_id>', methods=['GET', 'POST'])
def admin_cancel_movie(movie_id):
    movie_id = int(movie_id)
    movie = LincolnCinema.find_movie(movie_id)
    if movie.screenings:
        flash('Please cancel screening first.', 'error')
    else:
        # Cancel the movie by removing it from the list of movies
        LincolnCinema.cancel_movie(movie_id)
        # update movie status to inactive in movie json file
        Movie.update_movie_status_to_inactive(movie_id)
    return redirect(url_for("views.admin_home"))


# Route to add a new screening for a movie by admin
@views.route('/admin_add_screening/<int:movie_id>', methods=['GET', 'POST'])
def admin_add_screening(movie_id):
    # Get the movie based on its ID
    movie = LincolnCinema.find_movie(movie_id)
    movie_duration = movie.duration_in_mins
     # Get a list of hall names
    hall_name_list = [hall.hall_name for hall in LincolnCinema.all_halls]
    
    if request.method == 'POST':
        # Get screening information from the form
        screening_date = request.form['screening_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        hall_name = request.form['hall_name']
        price = round(float(request.form['price']), 2)
        print(price)
        # convert time to 24-hour format
        start_time = datetime.strptime(start_time, '%H:%M').strftime('%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M').strftime('%H:%M')        
        
        # Calculate the ending time based on start_time and movie.duration_in_minutes
        movie_duration_in_mins = int(movie.duration_in_mins) 

        start_datetime = datetime.strptime(start_time, '%H:%M')
        calculated_end_time = start_datetime + timedelta(minutes=movie_duration_in_mins)
        selected_end_datetime = datetime.strptime(end_time, '%H:%M')

        # Check if the selected end time is valid
        if selected_end_datetime <  calculated_end_time:
            flash('Invalid end time. Show time should be no shorter than Movie duration.', 'error')
            return render_template('admin_add_screening.html', movie=movie, hall_name_list=hall_name_list)
        
        # get hall object
        hall = LincolnCinema.find_hall(hall_name)
    
        # Create a Screening object
        seats = CinemaHallSeat.initialise_seats(hall, price)
        
        # Create a Screening object
        screening = Screening(movie_id, screening_date, start_time, end_time, hall, seats)

        # Add the screening to the movie object
        movie.add_screening(screening)

        # Get the seat data for this screening
        LincolnCinema.save_new_screening_to_json(screening)

        # Get a list of screening dates for the movie
        screening_date_list = movie.get_screening_date_list()
        
        # Filter the list of screenings to include only active screenings
        active_screenings = [screening for screening in movie.screenings if screening.is_active]

         # Redirect to the admin view movie details page
        return render_template('admin_view_movie_details.html', movie = movie, screening_date_list=screening_date_list, active_screenings=active_screenings)
    # Render the admin add screening page with movie and hall information
    return render_template('admin_add_screening.html', movie=movie, movie_duration=movie_duration, hall_name_list=hall_name_list)


# Route for displaying details of a screening, including customer bookings
@views.route('screening_booking_details/<movie_id>/<screening_id>')
def screening_booking_details(movie_id, screening_id):
    movie = LincolnCinema.find_movie(int(movie_id))
    screening = movie.find_screening(screening_id)
    all_customers = LincolnCinema.all_customers
    
    # Create lists to store customers who booked the screening and their paid bookings
    customers_who_booked_screening = []
    paid_bookings = []
    for customer in all_customers:
        for booking in customer.bookings():
            if booking.movie.id == int(movie_id) and booking.screening.screening_id == int(screening_id):
                customers_who_booked_screening.append(customer)
                if booking.status == 'Paid':
                    paid_bookings.append(booking)  # Add paid bookings to the list
    
    # Render the admin screening details page with the screening, movie, and related data
    return render_template('admin_screening_details.html', screening=screening, movie=movie,
                            customers_who_booked_screening=customers_who_booked_screening,
                            paid_bookings=paid_bookings)  # Pass the paid bookings to the template


# Route for processing a refund by an admin
@views.route('/admin_refund_booking/<int:booking_id>/<username>')
def admin_refund_booking(booking_id, username):
    # Find the customer
    customer = LincolnCinema.find_customer(username)
    # Find the booking to refund
    booking = customer.find_booking(booking_id)
    movie_id = booking.movie.id
    screening_id = booking.screening.screening_id
    payment_id = booking.payment.payment_id
    # Find the credit card payment associated with the booking
    creditcard_payment = LincolnCinema.find_payment(payment_id)

    if creditcard_payment is None:
        flash("Payment not found", 'error')

    # Process the refund and update related information
    is_success = creditcard_payment.process_refund()
    
    if is_success:
        reserved_seats_id = []
        for seat in booking.selected_seats:
            seat_id = seat.seat_id
            reserved_seats_id.append(seat_id)
            for screening_seat in booking.screening.seats:
                if screening_seat.seat_id == seat_id:
                    screening_seat.is_reserved = False
        is_reserved = False       
        Screening.update_reserved_seats_to_json(screening_id, reserved_seats_id, is_reserved)

        new_status = 'Refunded'
        booking.status = new_status
        Admin.cancel_booking(booking_id, new_status)

        # Create a confirmation notification
        confirmation_message = "Due to the screening cancellation, your booking has been refunded. We apologize for any inconvenience caused."
        notification = Notification(customer, "Refund Confirmation", confirmation_message, datetime.now(), booking)
        customer.add_notification(notification)

        # Save the confirmation notification to JSON
        Notification.save_notification_to_json(notification)

        # Use Flask's flash function to send the confirmation message
        flash("Booking has been refunded! A confirmation notice has been sent to the customer.", 'success')

    return redirect(url_for('views.screening_booking_details', movie_id=movie_id, screening_id=screening_id))


# Route for canceling a screening by an admin
@views.route('/admin_cancel_screening/<int:screening_id>/<int:movie_id>', methods=['GET', 'POST'])
def admin_cancel_screening(screening_id, movie_id):
    # Find the screening to cancel
    movie = LincolnCinema.find_movie(movie_id)

    # Find the screening to cancel within the movie
    screening = movie.find_screening(screening_id)

    if screening:
        # Check if there are reserved seats for the screening
        has_reserved_seats = any(seat.is_reserved for seat in screening.seats)

        if has_reserved_seats:
            flash('There are reserved seats for this screening. Please refund booking first.', 'error')
        else:
            # Set the screening as inactive and update it in JSON
            screening.is_active = False
            Screening.update_screening_status_to_inactive_to_json(screening_id)

            flash(f"Screening ID {screening_id} has been successfully cancelled.", 'success')
    else:
        flash(f"Screening with ID {screening_id} not found.", 'error')
     # Redirect to the movie details page
    return redirect(url_for('views.view_movie_details', movie_id=movie_id))



# ========= Customer Routes =========
# Route for the customer's home page
@views.route('/customer_home')
def customer_home():
    # Check if the user is logged in, if not, redirect to the login page
    if not g.user:
        return redirect(url_for('views.login'))
    # Get all movies, language, and genre lists
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    # Render the customer home page with the data
    return render_template('cus_home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list)


# Route for selecting seats for a movie screening
@views.route('/customer_select_seats/<movie_id>/<screening_date>/<start_time>', methods=['GET', 'POST'])
def customer_select_seats(movie_id, screening_date, start_time):
    # Find the screening based on screening_date and start_time
    movie = LincolnCinema.find_movie(int(movie_id))
    screening = LincolnCinema.find_screening_by_date_and_time(movie, screening_date, start_time)
    if request.method == 'POST':
        # Handle seat selection by customers
        current_date = datetime.now().date()
        selected_seats = request.form.get('selected_seats')
        if not selected_seats:
            flash('Please select at least one seat.', 'error')
        else:
            # Parse the selected seats
            selected_seats = json.loads(selected_seats)
            # Convert the list of dictionaries into a list of lists
            selected_seats_id_list = [str(seat['rowNumber'])+str(seat['seatNumber']) for seat in selected_seats]
            # get seat objects
            seat_objects = []
            for seat in screening.seats:
                for seat_id in selected_seats_id_list:
                    if seat.seat_id == seat_id:
                        seat_objects.append(seat)
            num_of_seats = len(seat_objects)
            # caculate total_price
            total_price = 0
            for seat in seat_objects:
                total_price += float(seat.seat_price)

            username = g.user.username
            customer = LincolnCinema.find_customer(username)
    
            status = 'Pending'
            # create book object
            new_booking = Booking(customer, movie, screening, num_of_seats, seat_objects, current_date, total_price, status)
            is_booking_repeated = customer.add_booking(new_booking)
            if is_booking_repeated:
                Booking.save_new_bookings_to_json(new_booking)
            else:
                flash('You have unpaid booking for this screening', 'error')
                return redirect(url_for('views.customer_select_seats', movie_id=movie_id, screening_date = screening_date,start_time=start_time ))                
            return render_template('cus_checkout.html', booking=new_booking)

    # Pass the screening object to the seat selection page
    return render_template('cus_select_seats.html', screening=screening, movie=movie)


# Route for validating a coupon for a booking
@views.route('/validate_coupon/<booking_id>', methods=['POST'])
def validate_coupon(booking_id):
    today_date = datetime.now()
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(int(booking_id))
    coupon_code = request.form.get('coupon_code')
    
    if booking.coupon:
        flash("Coupon has already been applied!", 'error')
    else:
        # get valid coupon codes
        valid_coupon_codes = []  
        for coupon in LincolnCinema.all_coupons:
            if coupon.expiration_date.date() >= today_date.date():
                valid_coupon_codes.append(coupon.coupon_code)
        coupon = LincolnCinema.find_coupon(coupon_code)
        # Check if the coupon code is valid and exists in the dummy_coupons dictionary
        if coupon_code in valid_coupon_codes:
            discount_percentage = coupon.discount_percentage
            discounted_price = booking.total_amount * (100 - discount_percentage)/100
            booking.total_amount = discounted_price
            booking.coupon = coupon
            # Redirect to the payment page with the valid coupon
            flash("Coupon is applied successfully!", 'success')
            return redirect(url_for('views.customer_apply_coupon', booking_id=booking_id))
        else:
            # Invalid coupon code, flash an error message and redirect back to the checkout page
            flash('Invalid or expired coupon code. Please try again.', 'error')
            return redirect(url_for('views.customer_apply_coupon', booking_id=booking_id))
    return redirect(url_for('views.customer_apply_coupon', booking_id=booking_id))


# Route for applying a coupon and finalizing the booking
@views.route('customer_apply_coupon/<booking_id>')
def customer_apply_coupon(booking_id):
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(booking_id)
    is_seats_available = LincolnCinema.check_seat_availability(booking)
    if is_seats_available == True: 
        return render_template('cus_checkout.html', booking=booking)
    else:
        flash('Seats have become unavailable. Please start a new booking and choose your seats again.', 'error')
        bookings = customer.bookings()
        return render_template('cus_bookings.html', bookings = bookings)


# Route for handling the payment process
@views.route('/customer_payment/<booking_id>', methods=['GET', 'POST'])
def customer_payment(booking_id):
    # Find the customer and the booking based on the provided booking ID
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(int(booking_id))
    coupon = booking.coupon
    if request.method == 'POST':
        # Check seat availability
        is_seats_available = LincolnCinema.check_seat_availability(booking)
        if is_seats_available == True: 
            # Get payment information from the form
            card_holder_name = request.form.get('card_holder_name')
            card_number = request.form.get('card_number')
            expire_date = request.form.get('expire_date')
            cvc = request.form.get('cvc')
            amount = request.form.get('amount')
            try:
                # Assuming the date format is MM/YYYY
                date_parts = expire_date.split('/')
                if len(date_parts) == 2:
                    month = int(date_parts[0])
                    year = int(date_parts[1])
                    expiry_date = datetime(year, month, 1)  # Set the day to 1 (the first day of the month)

                    # Check if the expiry date is in the future
                    if expiry_date > datetime.now():
                        formatted_expiry_date = expiry_date.strftime('%Y-%m')  # Format as 'YYYY-MM'
                        print('step1 is done')            
                        print('step2 is done')                 
                        # Create a CreditCard object
                        credit_card_payment = CreditCard(
                            payment_id=booking.booking_id,  # Use booking ID as payment ID, or provide a unique ID
                            amount=booking.total_amount,
                            created_on=datetime.now(),
                            coupon=coupon, 
                            credit_card_number=card_number,
                            card_type="Card Type Here",  # You should provide the card type
                            expiry_date=formatted_expiry_date,
                            name_on_card=card_holder_name
                        )
                        payment_id = credit_card_payment.payment_id
                        # Process the payment (you may add this logic in CreditCard.process_payment)
                        payment_successful = credit_card_payment.process_payment()
                        print(f'new credit card: {credit_card_payment}')         
                        if payment_successful == True:
                            # Assign the CreditCard object to the booking's payment attribute
                            booking.payment = credit_card_payment

                            # update the booking status
                            new_status = 'Paid'
                            movie_id = booking.movie.id
                            screening_id = booking.screening.screening_id
                            LincolnCinema.add_payment(credit_card_payment)
                            CreditCard.save_payment_to_json(credit_card_payment)  
                            booking.status = new_status
                            LincolnCinema.update_booking_payment_and_status(booking_id, payment_id, new_status)
                            
                            # Mark selected seats as reserved and update screening data
                            reserved_seats_id = []
                            for seat in booking.selected_seats:
                                for screening_seat in booking.screening.seats:
                                    if seat.seat_id == screening_seat.seat_id:
                                        screening_seat.is_reserved = True
                                        reserved_seats_id.append(seat.seat_id)
                                        print('seat reserved successfully!')
                            is_reserved = True       
                            Screening.update_reserved_seats_to_json(screening_id, reserved_seats_id, is_reserved)

                            # Redirect to a success or confirmation page
                            return redirect(url_for('views.customer_confirm_booking', booking_id=booking_id))
                        else:
                            flash('Payment processing failed. Please verify your payment information and try again. If the issue persists, please contact our customer support for assistance.', 'error')
                    else:
                        flash('Card has expired. Please use a valid card.', 'error')
                else:
                    # Handle invalid date format
                    flash('Please enter a valid expiry date in MM/YYYY format.', 'error')

            except ValueError:
                # Handle invalid date format or other errors
                flash('Invalid date format. Please enter a valid expiry date.', 'error')
        else:
            flash('Seats have become unavailable. Please start a new booking and choose your seats again.', 'error')
            bookings = customer.bookings()
            return render_template('cus_bookings.html', bookings = bookings)
    return render_template('cus_payment.html', booking=booking)


# Route for displaying the customer's bookings
@views.route('customer_bookings')
def customer_bookings():
    # Find the customer based on the currently logged-in user
    customer = LincolnCinema.find_customer(g.user.username)
    # Retrieve the customer's bookings
    bookings = customer.bookings()
    return render_template('cus_bookings.html', bookings = bookings)


# Route for canceling a booking
@views.route('customer_cancel_booking/<booking_id>')
def customer_cancel_booking(booking_id):
    # Find the customer based on the currently logged-in user
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(booking_id)
    # Cancel the booking and update its status
    customer.cancel_booking(booking_id)
    bookings = customer.bookings()
    new_status = 'Canceled'
    LincolnCinema.update_status_to_canceled(booking_id, new_status)
    
    # Create a confirmation notification
    confirmation_message = "Your booking has been canceled!"
    notification = Notification(customer, "Cancel Confirmation", confirmation_message, datetime.now(), booking)
    customer.add_notification(notification)
    # Save the confirmation notification to JSON
    Notification.save_notification_to_json(notification)

    # Use Flask's flash function to send the confirmation message
    flash("Your booking has been canceled! A confirmation notice has been sent to you!", 'success')  # You can use 'success' or any other category
    
    return render_template('cus_bookings.html', bookings = bookings)


# Route for confirming a booking
@views.route('/customer_confirm_booking/<booking_id>')
def customer_confirm_booking(booking_id):
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(booking_id)

    # Create a confirmation notification
    confirmation_message = "Your booking has been confirmed! Thank you for choosing Lincoln Cinema."
    notification = Notification(customer, "Booking Confirmation", confirmation_message, datetime.now(), booking)
    customer.add_notification(notification)
    # Save the confirmation notification to JSON
    Notification.save_notification_to_json(notification)

    # Use Flask's flash function to send the confirmation message
    flash("Your booking has been confirmed! A confirmation notice has been sent to you!", 'success')  # You can use 'success' or any other category
    
    return render_template("cus_confirm_booking.html", booking=booking)


# Route for displaying customer notifications
@views.route('customer_notifications')
def customer_notifications():
    customer = LincolnCinema.find_customer(g.user.username)
    notifications = customer.notifications
    # Sort the notifications by date_time in descending order
    notifications = sorted(notifications, key=lambda notification: notification.date_time, reverse=True)
    return render_template('cus_notifications.html', notifications=notifications)


# Route for displaying details of a customer's booking
@views.route('customer_booking_details/<booking_id>')
def customer_booking_details(booking_id):
    customer = LincolnCinema.find_customer(g.user.username)
    booking = customer.find_booking(booking_id)    
    return render_template("cus_booking_details.html", booking=booking)
    


# ========= Staff Routes ==========
# Routes for staff home
@views.route('/staff_home')
def staff_home():
    if not g.user:
        return redirect(url_for('views.login'))
    all_movies = LincolnCinema.all_movies
    language_list = LANGUAGE_LIST
    genre_list = GENRE_LIST
    return render_template('staff_home.html', all_movies=all_movies, language_list=language_list, genre_list=genre_list)

# Routes for staff view all bookings
@views.route('/staff_view_bookings')
def staff_view_bookings():
    # get all bookings
    all_bookings = []
    all_customers = LincolnCinema.all_customers
    for customer in all_customers:
        for booking in customer.bookings():
            all_bookings.append(booking)    
    return render_template('staff_view_bookings.html', all_bookings=all_bookings)


# Routes for staff refund a booking
@views.route('/staff_refund_booking/<int:booking_id>/<username>')
def staff_refund_booking(booking_id, username):
    # Find the customer based on the provided username
    customer = LincolnCinema.find_customer(username)
    if customer is None:
        flash("Customer not found", 'error')
    # Find the booking to refund within the customer's bookings
    booking = customer.find_booking(booking_id)
    if booking is None:
        flash("Booking not found", 'error')
    # Retrieve movie and screening information
    movie_id = booking.movie.id
    screening_id = booking.screening.screening_id
    creditcard_payment = booking.payment

    if creditcard_payment is None:
        flash("Payment not found", 'error')
        return redirect(url_for('views.some_error_route'))  # Handle error redirection
    # Process the refund and update related information
    is_success = creditcard_payment.process_refund()
    
    if is_success:
        reserved_seats_id = []
        for seat in booking.selected_seats:
            seat_id = seat.seat_id
            reserved_seats_id.append(seat_id)
            for screening_seat in booking.screening.seats:
                if screening_seat.seat_id == seat_id:
                    screening_seat.is_reserved = False
        is_reserved = False       
        Screening.update_reserved_seats_to_json(screening_id, reserved_seats_id, is_reserved)

        new_status = 'Refunded'
        booking.status = new_status
        FrontDeskStaff.cancel_booking(booking_id, new_status)

        # Create a confirmation notification
        confirmation_message = "Your booking has been refunded successffully."
        notification = Notification(customer, "Refund Confirmation", confirmation_message, datetime.now(), booking)
        customer.add_notification(notification)

        # Save the confirmation notification to JSON
        Notification.save_notification_to_json(notification)

        # Use Flask's flash function to send the confirmation message
        flash("Booking has been refunded! A confirmation notice has been sent to the customer.", 'success')

    return redirect(url_for('views.staff_view_bookings'))


# Route for searching and displaying a customer's bookings for staff
@views.route('/staff_search_customer', methods=['POST'])
def staff_search_customer():
    username = request.form.get('username')
    try:
        # Implement the search logic here to filter customers by username
        customer = LincolnCinema.find_customer(username)
        if customer is None:
            flash('Customer not found', 'error')
            return redirect(url_for('views.staff_view_bookings'))
         # Retrieve all bookings for the found customer
        all_bookings = customer.bookings()
        return render_template('staff_view_bookings.html', all_bookings=all_bookings)
    except Exception as e:
        flash('An error occurred while searching for the customer.', 'error')
        app.logger.error(str(e))
        return redirect(url_for('views.staff_view_bookings'))


# Route for selecting seats for staff
@views.route('/staff_select_seats/<movie_id>/<screening_date>/<start_time>', methods=['GET', 'POST'])
def staff_select_seats(movie_id, screening_date, start_time):
    # Find the screening based on screening_date and start_time
    all_customers_username = [customer.username for customer in LincolnCinema.all_customers]
    movie = LincolnCinema.find_movie(int(movie_id))
    screening = LincolnCinema.find_screening_by_date_and_time(movie, screening_date, start_time)
    if request.method == 'POST':
        # Handle seat selection by customers
        current_date = datetime.now().date()
        selected_seats = request.form.get('selected_seats')
        customer_username = request.form.get('username')
        customer = LincolnCinema.find_customer(customer_username)
        if not customer_username:
            flash('Please select a Customer', 'error')
            return render_template('staff_select_seats.html', screening=screening, movie=movie,
                           all_customers_username=all_customers_username)

        if not selected_seats:
            flash('Please select at least one seat.', 'error')
        else:
            # Parse the selected seats
            selected_seats = json.loads(selected_seats)
            # Convert the list of dictionaries into a list of lists
            selected_seats_id_list = [str(seat['rowNumber'])+str(seat['seatNumber']) for seat in selected_seats]
            # get seat objects
            seat_objects = []
            for seat in screening.seats:
                for seat_id in selected_seats_id_list:
                    if seat.seat_id == seat_id:
                        seat_objects.append(seat)
            num_of_seats = len(seat_objects)
            # caculate total_price
            total_price = 0
            for seat in seat_objects:
                total_price += float(seat.seat_price)    
            status = 'Pending'
            # create book object
            new_booking = Booking(customer, movie, screening, num_of_seats, seat_objects, current_date, total_price, status)
            is_booking_repeated = customer.add_booking(new_booking)
            if is_booking_repeated:
                Booking.save_new_bookings_to_json(new_booking)
            else:
                flash(f'{customer.name} have unpaid booking for this screening', 'error')
                return redirect(url_for('views.staff_select_seats', movie_id=movie_id, screening_date = screening_date,start_time=start_time ))                
            return render_template('staff_checkout.html', booking=new_booking)

    # Pass the screening object to the seat selection page
    return render_template('staff_select_seats.html', screening=screening, movie=movie,
                           all_customers_username=all_customers_username)


# Route for staff to validate a coupon during checkout
@views.route('/staff_validate_coupon', methods=['POST'])
def staff_validate_coupon():
    today_date = datetime.now()
    coupon_code = request.form.get('coupon_code')
    username = request.form.get('username')
    booking_id = request.form.get('booking_id')
    customer = LincolnCinema.find_customer(username)
    booking = customer.find_booking(int(booking_id))
    
    if booking.coupon:
        flash("Coupon has already been applied!", 'error')
    else:
        # get valid coupon codes
        valid_coupon_codes = []  
        for coupon in LincolnCinema.all_coupons:
            if coupon.expiration_date.date() >= today_date.date():
                valid_coupon_codes.append(coupon.coupon_code)
        coupon = LincolnCinema.find_coupon(coupon_code)
        # Check if the coupon code is valid and exists in the dummy_coupons dictionary
        if coupon_code in valid_coupon_codes:
            discount_percentage = coupon.discount_percentage
            discounted_price = booking.total_amount * (100 - discount_percentage)/100
            booking.total_amount = discounted_price
            booking.coupon = coupon
            # Redirect to the payment page with the valid coupon
            flash("Coupon is applied successfully!", 'success')
            return redirect(url_for('views.staff_apply_coupon', booking_id=booking_id, username = username))
        else:
            # Invalid coupon code, flash an error message and redirect back to the checkout page
            flash('Invalid or expired coupon code. Please try again.', 'error')
            return redirect(url_for('views.staff_apply_coupon', booking_id=booking_id, username = username))
    return redirect(url_for('views.staff_apply_coupon', booking_id=booking_id, username = username))


# Route for staff to apply a coupon and proceed to checkout
@views.route('staff_apply_coupon/<booking_id>/<username>')
def staff_apply_coupon(booking_id, username):
    customer = LincolnCinema.find_customer(username)
    booking = customer.find_booking(booking_id)
    is_seats_available = LincolnCinema.check_seat_availability(booking)
    if is_seats_available == True: 
        return render_template('staff_checkout.html', booking=booking, customer=customer)
    else:
        flash('Seats have become unavailable. Please choose seats again.', 'error')
        return redirect(url_for('views.staff_view_bookings'))
    

# Route for staff to process a payment for a booking
@views.route('/staff_payment/<booking_id>/<username>', methods=['GET', 'POST'])
def staff_payment(booking_id, username):
    print(f"username....{username}")
    customer = LincolnCinema.find_customer(username)
    booking = customer.find_booking(int(booking_id))
    coupon = booking.coupon
    if request.method == 'POST':
        # Check seat availability
        is_seats_available = LincolnCinema.check_seat_availability(booking)
        if is_seats_available == True: 
            card_holder_name = request.form.get('card_holder_name')
            card_number = request.form.get('card_number')
            expire_date = request.form.get('expire_date')
            cvc = request.form.get('cvc')
            amount = request.form.get('amount')
            try:
                # Assuming the date format is MM/YYYY
                date_parts = expire_date.split('/')
                if len(date_parts) == 2:
                    month = int(date_parts[0])
                    year = int(date_parts[1])
                    expiry_date = datetime(year, month, 1)  # Set the day to 1 (the first day of the month)

                    # Check if the expiry date is in the future
                    if expiry_date > datetime.now():
                        formatted_expiry_date = expiry_date.strftime('%Y-%m')  # Format as 'YYYY-MM'
                        print('step1 is done')            
                        print('step2 is done')                 
                        # Create a CreditCard object
                        credit_card_payment = CreditCard(
                            payment_id=booking.booking_id,  # Use booking ID as payment ID, or provide a unique ID
                            amount=booking.total_amount,
                            created_on=datetime.now(),
                            coupon=coupon, 
                            credit_card_number=card_number,
                            card_type="Card Type Here",  # You should provide the card type
                            expiry_date=formatted_expiry_date,
                            name_on_card=card_holder_name
                        )
                        payment_id = credit_card_payment.payment_id
                        # Process the payment (you may add this logic in CreditCard.process_payment)
                        payment_successful = credit_card_payment.process_payment()
                        print(f'new credit card: {credit_card_payment}')         
                        if payment_successful == True:
                            # Assign the CreditCard object to the booking's payment attribute
                            booking.payment = credit_card_payment

                            # You may also update the booking status here
                            new_status = 'Paid'
                            movie_id = booking.movie.id
                            screening_id = booking.screening.screening_id
                            LincolnCinema.add_payment(credit_card_payment)
                            CreditCard.save_payment_to_json(credit_card_payment)  
                            booking.status = new_status
                            LincolnCinema.update_booking_payment_and_status(booking_id, payment_id, new_status)
                            
                            reserved_seats_id = []
                            for seat in booking.selected_seats:
                                for screening_seat in booking.screening.seats:
                                    if seat.seat_id == screening_seat.seat_id:
                                        screening_seat.is_reserved = True
                                        reserved_seats_id.append(seat.seat_id)
                                        print('seat reserved successfully!')
                            is_reserved = True       
                            Screening.update_reserved_seats_to_json(screening_id, reserved_seats_id, is_reserved)

                            # Redirect to a success or confirmation page
                            return redirect(url_for('views.staff_confirm_booking', booking_id=booking_id, username=username))
                        else:
                            flash('Payment processing failed. Please verify your payment information and try again. If the issue persists, please contact our customer support for assistance.', 'error')
                    else:
                        flash('Card has expired. Please use a valid card.', 'error')
                else:
                    # Handle invalid date format
                    flash('Please enter a valid expiry date in MM/YYYY format.', 'error')

            except ValueError:
                # Handle invalid date format or other errors
                flash('Invalid date format. Please enter a valid expiry date.', 'error')
        else:
            flash('Seats have become unavailable. Please start a new booking and choose your seats again.', 'error')
            return render_template('staff_home.html')
    return render_template('staff_payment.html', booking=booking, username = username)


# Route for staff cancel booking
@views.route('staff_cancel_booking/<booking_id>/<username>')
def staff_cancel_booking(booking_id, username):
    customer = LincolnCinema.find_customer(username)
    booking = customer.find_booking(booking_id)
    customer.cancel_booking(booking_id)
    bookings = customer.bookings()
    new_status = 'Canceled'
    LincolnCinema.update_status_to_canceled(booking_id, new_status)
    
    # Create a confirmation notification
    confirmation_message = "Your booking has been canceled!"
    notification = Notification(customer, "Cancel Confirmation", confirmation_message, datetime.now(), booking)
    customer.add_notification(notification)
    # Save the confirmation notification to JSON
    Notification.save_notification_to_json(notification)

    # Use Flask's flash function to send the confirmation message
    flash(f"{customer.name}'s booking has been canceled! A confirmation notice has been sent to {customer.name}!", 'success')  # You can use 'success' or any other category
    
    return redirect(url_for('views.staff_view_bookings'))


# Route for staff confirm booking 
@views.route('/staff_confirm_booking/<booking_id>/<username>')
def staff_confirm_booking(booking_id, username):
    customer = LincolnCinema.find_customer(username)
    booking = customer.find_booking(booking_id)

    # Create a confirmation notification
    confirmation_message = "Your booking has been confirmed! Thank you for choosing Lincoln Cinema."
    notification = Notification(customer, "Booking Confirmation", confirmation_message, datetime.now(), booking)
    customer.add_notification(notification)
    # Save the confirmation notification to JSON
    Notification.save_notification_to_json(notification)

    # Use Flask's flash function to send the confirmation message
    flash("Your booking has been confirmed! A confirmation notice has been sent to you!", 'success')  # You can use 'success' or any other category
    
    return render_template("staff_confirm_booking.html", booking=booking)



