"""! @brief Cinema Controller Module"""

##
# @mainpage Lincoln Cinema Online Movie Ticket System Documentation
#
# @section description_main Description
# Welcome to the Doxygen documentation for the Lincoln Cinema Online Movie Ticket System. 
# This documentation provides an overview of the system's architecture and components. 
# Please note that this codebase represents a skeleton Python code, outlining the 
# structure of the system with method signatures and type hints.
# The Lincoln Cinema Online Movie Ticket System follows the Model-View-Controller 
# (MVC) design pattern. It separates the system into Model (data and business logic), 
# View (user interface), and Controller (user interaction) components. 
# Each module plays a crucial role in achieving a structured and maintainable 
# software solution for online movie ticket booking.
# Explore the following sections to understand the purpose and responsibilities 
# of each component:
# - [models.py](models_8py.html): Defines data models for the system, including customers, staff, movies, and more.
# - [controller.py](controller_8py.html): Implements the Controller component, managing 
# user interactions, data management, and core functionalities such as user registration, movie management, and booking creation.
# 
# @section notes_main Notes
# - This codebase serves as a foundational framework for the Lincoln Cinema Online Movie Ticket System. It includes method 
# signatures (method name, parameters, return types) without full implementations.
# - The code will be completed by implementing the methods according to project requirements.
# - The system's architecture follows the Model-View-Controller (MVC) pattern, promoting separation of concerns and maintainability.
# - Please refer to the individual method signatures and descriptions for guidance on functionality and usage.
# - As development progresses, additional functionalities and features will be added to this skeleton codebase.
# For detailed information on each module, classes, methods, and their intended functionality, please navigate through the documentation.

##
# @file controller.py
#
# @brief Cinema Controller Module
#
# @section description_controller Description
# The `controller.py` file defines the CinemaController class, 
# which acts as the controller component in a Model-View-Controller (MVC) 
# architecture for an online movie ticket system. This controller is responsible 
# for managing user interactions, data management, and core functionalities.
# It handles tasks such as user registration, movie management, booking creation, 
# payment processing, and communication with other system components. 
# Additionally, it provides functions to retrieve information about movies, 
# screenings, and bookings, as well as perform various administrative tasks 
# like adding movies, canceling screenings, and processing payments. 
# The file also includes functions for sending notifications to customers 
# and validating coupon codes.
#
# @section notes_clinic Notes
# - This controller class plays a central role in managing the online movie ticket system. It serves as the bridge between user interactions and data handling, ensuring smooth operation.
# - Consider implementing the `read_data_from_file` function to load initial data from a file or database when the system starts up. This will populate the object lists, making them ready for use.
# - The authentication-related functions (`register_customer` and `login_user`) are essential for user management. Ensure robust user authentication and error handling to enhance system security.
# - When adding or canceling movies and screenings using the admin-related functions, consider implementing proper access control mechanisms to restrict these operations to authorized administrators only.
# - The `create_booking` function is crucial for allowing customers to book movie tickets. Ensure that it handles seat availability, payment processing, and coupon validation effectively.
# - The refund functionality (`refund_customer`) should be implemented carefully to ensure accurate refunds to customers in case of booking cancellations.
# - The `calculate_total_amount` function plays a role in determining the total cost of a booking, considering selected seats and applied coupons. Ensure that it calculates prices accurately and consistently.
# - The `send_notification` function is vital for communicating with customers. Use it to send important updates, promotions, or booking confirmations.
# - Regularly update and maintain this controller class as the online movie ticket system evolves. Ensure that it remains aligned with the MVC architecture and follows best coding practices.
#
# @section author_cinema Author
# Created by Elaine Xu on 28/09/2023


# Imports
from .models import *


class CinemaController:
    """! The CinemaController class manages cinema-related data and operations. """
    def __init__(self):
        """! Constructor for the CinemaController class.
        Initializes lists for customers, admins, front desk staff, movies, halls, coupons, and payments.
        """
        self.__customers = []
        self.__admins = []
        self.__front_desk_staffs = []
        self.__movies = []
        self.__halls = []
        self.__coupons = []
        self.__payments = []
    

    # =========== Methods to get controller object list ==========
    @property
    def all_admins(self):
        """! Get a list of all admin objects.
        @return (list): A list of all admin objects.
        """
        return self.__admins


    @property
    def all_front_desk_staffs(self):
        """! Get a list of all front desk staff objects.
        @return (list): A list of all front desk staff objects.
        """
        return self.__front_desk_staffs
    

    @property
    def all_customers(self):
        """! Get a list of all customer objects.
        @return (list): A list of all customer objects.
        """
        return self.__customers


    @property
    def all_movies(self):
        """! Get a list of all movie objects.
        @return (list): A list of all movie objects.
        """
        return self.__movies
    

    @property
    def all_halls(self):
        """! Get a list of all hall objects.
        @return (list): A list of all hall objects.
        """
        return self.__halls
    

    @property
    def all_coupons(self):
        """! Get a list of all coupon objects.
        @return (list): A list of all coupon objects.
        """
        return self.__coupons
    

    @property
    def all_payments(self):
        """! Get a list of all payment objects.
        @return (list): A list of all payment objects.
        """
        return self.__payments



    # ============ methods to find objects from controller ============
    def find_admin(self, username: str):
        """! Find an admin by its username.
        @param username (str): The ID to search for.
        @return (Customer): The admin object if found, or None.
        """
        for admin in self.all_admins:
            if admin.username == username:
                return admin
        return None
    

    def find_staff(self, username: str):
        """! Find a staff by its username.
        @param username (str): The ID to search for.
        @return (Customer): The staff object if found, or None.
        """
        for staff in self.all_front_desk_staffs:
            if staff.username == username:
                return staff
        return None
    

    def find_customer(self, username: str):
        """! Find a customer by its username.
        @param username (str): The ID to search for.
        @return (Customer): The customer object if found, or None.
        """
        for customer in self.all_customers:
            if customer.username == username:
                return customer
        return None


    def find_movie(self, movie_id: int):
        """! Find a movie by its ID.
        @param id (int): The ID to search for.
        @return (Movie): The movie object if found, or None.
        """
        for movie in self.__movies:
            if movie.id == movie_id:
                return movie
        return None
    

    def find_hall(self, hall_name):
        """! Find a hall by its name.
        @param hall_name (str): The name of the hall to search for.
        @return (Hall): The hall object if found, or None.
        """
        for hall in self.__halls:
            if hall.hall_name == hall_name:
                return hall
        return None
    

    def find_coupon(self, coupon_code):
        """! Find a coupon by its code.
        @param coupon_code (str): The coupon code to search for.
        @return (Coupon): The coupon object if found, or None.
        """
        for coupon in self.all_coupons:
            if coupon.coupon_code == coupon_code:
                return coupon 
        return None


    def find_payment(self, new_payment_id):
        """! Find a payment by its ID.
        @param new_payment_id (int): The payment ID to search for.
        @return (Payment): The payment object if found, or None.
        """
        for payment in self.all_payments:
            if payment.payment_id == new_payment_id:
                return payment
        return None
    
        
    def get_language_list(self):
        """! Get a list of unique languages from the movies.
        @return: A list of unique languages used in the movies.
        """
        language_list = []
        for movie in self.all_movies:
            if movie.language not in language_list:
                language_list.append(movie.language)
        return language_list
    

    def get_genre_list(self):
        """! Get a list of unique genres from the movies.
        @return: A list of unique genres used in the movies.
        """
        genre_list = []
        for movie in self.all_movies:
            if movie.genre not in genre_list:
                genre_list.append(movie.genre)
        return genre_list


    def find_screening_by_date_and_time(self, movie, screening_date, start_time):
        """! Find a screening for a given movie based on date and start time.

        @param movie: The movie object to search for a screening.
        @param screening_date: The date of the screening to search for.
        @param start_time: The start time of the screening to search for.

        @return: The matching screening object if found, or None if not found.
        """
        # Convert the input values to datetime objects
        # Iterate through the movie's screenings to find a matching screening
        for screening in movie.screenings:
            if (
                screening.screening_date == screening_date and
                screening.start_time == start_time
            ):
                return screening

        # If no matching screening is found, return None
        return None
    


    # ========== methods to append new object ===========
    def add_customer(self, customer):
        """! Add a customer to the list of customers.
        @param customer: The customer object to be added.
        """
        self.__customers.append(customer)
    

    def add_admin(self, admin):
        """! Add an admin to the list of admins.
        @param admin: The admin object to be added.
        """
        self.__admins.append(admin)


    def add_front_desk_staff(self, front_desk_staff):
        """! Add a front desk staff member to the list of front desk staff.
        @param front_desk_staff: The front desk staff object to be added.
        """
        self.__front_desk_staffs.append(front_desk_staff)


    def add_movie(self, movie_object):
        """! Add a movie to the list of movies.
        @param movie_object: The movie object to be added.
        """
        self.__movies.append(movie_object)


    def add_hall(self, hall_object):
        """! Add a hall to the list of halls.
        @param hall_object: The hall object to be added.
        """
        self.__halls.append(hall_object)


    def add_payment(self, a_payment):
        """! Add a payment to the list of payments.
        @param a_payment: The payment object to be added.
        """
        self.__payments.append(a_payment)
            

    def add_coupon(self, coupon):
        """! Add a coupon to the list of coupons.
        @param coupon: The coupon object to be added.
        """
        self.__coupons.append(coupon)


    # ============ Other methods ================
    def register_customer(self, name, address, email, phone, username, hashed_password) -> bool:
        """! Register a new customer and store their information."""
        # Check if the username already exists
        if self.find_customer(username):
            return False
        new_customer = Guest.register(name, address, email, phone, username, hashed_password)
        self.add_customer(new_customer)
        print(f'new customer{new_customer}')
        return True


    def check_duplicate_username(self, username):
        """! Find a customer by their username.
        @param username (str): The username to search for.
        @return (Customer): The customer object if found, or None.
        """
        for customer in self.__customers:
            if customer.username == username:
                return True
        return False
    

    def check_duplicate_email(self, email):
        """! Find a customer by their username.
        @param username (str): The username to search for.
        @return (Customer): The customer object if found, or None.
        """
        for customer in self.__customers:
            if customer.email == email:
                return True
        return False

    
    def validate_coupon(self, coupon_code):
        """! Validate a coupon code and check if it's still valid.
        @param coupon_code: The coupon code to validate.
        @return: True if the coupon code is valid, False if it's not valid.
        """
        today_date = datetime.now()        
        # get valid coupon codes
        valid_coupon_codes = []  
        for coupon in self.all_coupons:
            if coupon.expiration_date.date() >= today_date.date():
                valid_coupon_codes.append(coupon.coupon_code)
        coupon = self.find_coupon(coupon_code)


    def check_seat_availability(self, booking):
        """! Check seat availability for a booking.
        @param booking: The booking object for which seat availability is checked.
        @return: True if the selected seats are available, False if any seat is already reserved.
        """
        selected_seats = booking.selected_seats
        screening = booking.screening
        reserved_seats = [seat.seat_id for seat in screening.seats if seat.is_reserved == True]
    
        for selected_seat in selected_seats:
            if selected_seat.seat_id in reserved_seats:
                return False
        
        return True
    


    # ========== filter movies ==========       
    def customer_filter_movies(self, title, selected_language, selected_genre, date_from, date_to, user):
        """! Filter movies for a customer based on title, language, genre, and date range.

        @param title: The title of the movie to filter by.
        @param selected_language: The selected language to filter by.
        @param selected_genre: The selected genre to filter by.
        @param date_from: The start date of the date range to filter by.
        @param date_to: The end date of the date range to filter by.
        @param customer: The customer performing the filtering.

        @return: A list of filtered movies that match the criteria.
        """
        filtered_movies = self.all_movies
        if title:
            filtered_movies = user.search_movie_title(title, filtered_movies)
        if selected_language:
            if selected_language == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = user.search_movie_lang(selected_language, filtered_movies)
        if selected_genre:
            if selected_genre == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = user.search_movie_genre(selected_genre, filtered_movies)
        if not date_from or not date_to:
            filtered_movies = filtered_movies
        else:
            filtered_movies = user.search_movie_date(date_from, date_to, filtered_movies)
        return filtered_movies


    # ============= update database info ==============
    def save_new_bookings_to_json(self, booking):
        """! Save a new booking to a JSON file.
        @param booking: The booking object to be saved.
        """
        self.save_new_bookings_to_json(booking)


    def reserve_seats(self, booking):
        reserved_seats_id = []
        for seat in booking.selected_seats:
            for screening_seat in booking.screening.seats:
                if seat.seat_id == screening_seat.seat_id:
                    screening_seat.is_reserved = True
                    reserved_seats_id.append(seat.seat_id)
                    print('seat reserved successfully!')
        is_reserved = True  
        screening_id = booking.screening.screening_id
        Screening.update_reserved_seats_to_json(screening_id, reserved_seats_id, is_reserved)



    def cancel_movie(self, movie_id:int):
        """! Cancel a movie based on its ID.
        @param movie_id (int): The ID of the movie to cancel.
        """
        # Find the movie by its ID in the movies list
        movie_to_cancel = None
        for movie in self.all_movies:
            if movie.id == movie_id:
                movie_to_cancel = movie
                break

        if movie_to_cancel:
            # Remove the movie from the movies list
            movie_to_cancel.deactivate()

            # Update the JSON file to remove the canceled movie
            Movie.update_movies_json(self.all_movies)


    def update_booking_payment_and_status(self, booking_id, payment_id, new_status, payment_method):
        """! Update the payment and status of a booking.
        @param booking_id: The ID of the booking to update.
        @param payment_id: The ID of the associated payment.
        @param new_status: The new status of the booking.
        """
        Booking.update_payment_and_status(booking_id, payment_id, new_status, payment_method)
    
    
    def update_booking_payment_method(self, booking_id, payment_method, new_status):
        """! Update the payment and status of a booking.
        @param booking_id: The ID of the booking to update.
        @param payment_id: The ID of the associated payment.
        @param new_status: The new status of the booking.
        """
        Booking.update_payment_method(booking_id, payment_method, new_status)


    def update_status_to_canceled(self, booking_id, new_status):
        """! Update the status of a booking to 'canceled'.
        @param booking_id: The ID of the booking to update.
        @param new_status: The new status to set, which should be 'canceled'.
        """
        Booking.update_status_to_canceled(booking_id, new_status)

        
    def save_new_screening_to_json(self, new_screening):
        """! Save a new screening to a JSON file.
        @param new_screening: The new screening object to be saved.
        """
        Screening.save_new_screening_to_json(new_screening)



    # ============ Initialise Database =============
    def initialise_bookings(self):
        """! Create booking objects and add them to the corresponding customer records.
        @param username: The username of the customer to associate the bookings with.
        """
        bookings_info = Booking.read_from_file(BOOKINGS_FILENAME)
        for booking_info in bookings_info:
            for customer in self.all_customers:
                if booking_info["customer_username"] == customer.username:
                    # find customer
                    customer = self.find_customer(booking_info["customer_username"])

                    # Convert the movie_id from string to integer
                    movie_id = int(booking_info["movie_id"])
                    movie = self.find_movie(movie_id)

                    screening_id = int(booking_info["screening_id"])
                    screening = movie.find_screening(screening_id)
                    if screening is None:
                        print(f"screening with ID {screening_id} not found.")

                    num_of_seats = booking_info["num_of_seats"]
                    selected_seats_id_list = booking_info["selected_seats"]
                    selected_seats = []
                    for seat_id in selected_seats_id_list:
                        seat = screening.find_seat_by_id(int(seat_id))
                        if seat:
                            selected_seats.append(seat)
                        else:
                            print(f"Seat with ID {seat_id} not found for booking {booking_info['booking_id']}.")

                    created_on = date.fromisoformat(booking_info["created_on"])
                    total_amount = float(booking_info["total_amount"])
                    status = booking_info["status"]
                    print(status)
                    payment_method = booking_info["payment_method"]
                    payment_id = booking_info["payment_id"]
                    if payment_id:
                        payment = self.find_payment(int(payment_id))
                    else:
                        payment = None

                    booking = Booking(
                        customer=customer,
                        movie=movie,
                        screening=screening,
                        num_of_seats=num_of_seats,
                        selected_seats=selected_seats,
                        created_on=created_on,
                        total_amount=total_amount,
                        status=status,
                        payment_method=payment_method,
                        payment=payment)
                    customer.add_booking(booking)


    def initialise_payments(self):
        """! Create Payment objects from payment data and add them to the list of payments.
        """
        payments_data = Payment.read_payments_from_file()
        for item in payments_data:
            payment_id = item.get('payment_id')
            amount = item.get('amount')
            coupon_code = item.get('coupon')
            created_on_str = item.get('created_on')
            credit_card_number = item.get('credit_card_number')
            card_type = item.get('card_type')
            expiry_date_str = item.get('expiry_date')
            name_on_card = item.get('name_on_card')
            
            # Convert strings to appropriate data types
            created_on = datetime.strptime(created_on_str, '%Y-%m-%d %H:%M:%S')
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m')
            
            # Create a Coupon object if coupon data is provided
            coupon = None
            if coupon_code:
                coupon = self.find_coupon(coupon_code)
            
            # Create a Payment object and add it to the list
            payment = CreditCard(payment_id, amount, coupon, created_on, credit_card_number, card_type, expiry_date, name_on_card)
            self.__payments.append(payment)


    def initialise_movies(self):
        """! Create Movie objects from movie data and add them to the list of movies.
        """
        movies_data = Movie.read_from_file(MOVIES_FILENAME)
        for movie_info in movies_data:
            title = movie_info.get("title", "")
            language = movie_info.get("language", "")
            genre = movie_info.get("genre", "")
            country = movie_info.get("country", "")
            release_date = movie_info.get("release_date", "")
            duration_in_minutes = movie_info.get("duration", 0)  
            description = movie_info.get("description", "")
            movie_object = Movie(title, language, genre, country, release_date, duration_in_minutes, description)
            self.add_movie(movie_object)


    def initialise_screenings(self):
        """! Add screenings to their respective movies.
        Iterate through screening data and associate screenings with their movies.
        """
        screening_data_list = Screening.read_from_file(SCREENINGS_FILENAME)
        for screening_data in screening_data_list:
            movie_id = screening_data["movie_id"]
            movie = self.find_movie(int(movie_id))

            if movie:
                screening_date = screening_data["screening_date"]
                start_time = screening_data["start_time"]
                end_time = screening_data["end_time"]
                hall_name = screening_data["hall_name"]
                seats_data = screening_data.get("seats", [])

                hall = self.find_hall(hall_name)

                seats = []
                for seat_data in seats_data:
                    seat_number = seat_data.get("seat_number")
                    row_number = seat_data.get("row_number")
                    is_reserved = seat_data.get("is_reserved")
                    seat_price = seat_data.get("seat_price")

                    seat = CinemaHallSeat(seat_number, row_number, is_reserved, seat_price)
                    seats.append(seat)

                is_active = screening_data["is_active"]  # Use the correct attribute name
                screening = Screening(movie_id, screening_date, start_time, end_time, hall, seats, is_active)
                movie.add_screening(screening)
                print(screening.screening_id)
                print(f'just to check {movie.screenings}')
            else:
                print(f"Movie with ID {movie_id} not found.")


    def initialise_coupons(self):
        """! Read coupons data from a file and add them to the list of coupons.
        """
        coupons = Coupon.read_coupons_from_json()
        for coupon in coupons:
            self.__coupons.append(coupon)


    def initialise_notifications(self):
        """! Create Notification objects and add them to the corresponding customer records.
        @param username: The username of the customer to associate notifications with.
        """
        notification_data = Notification.read_from_file(NOTIFICATION_FILENAME)
        for data in notification_data:
            for customer in self.all_customers:
                if data["customer_username"] == customer.username:
                    date_time = datetime.strptime(data["date_time"], '%Y-%m-%d %H:%M:%S.%f')
                    booking_id = data["booking_id"]

                    # Find the booking by booking_id
                    booking = None
                    if booking_id is not None:
                        booking = customer.find_booking(booking_id)
                        if booking is None:
                            print(f"Booking with ID {booking_id} not found.")

                    # Create and add the notification to the customer
                    notification = Notification(
                        customer=customer,
                        subject=data["subject"],
                        message=data["message"],
                        date_time=date_time,
                        booking=booking
                    )

                    customer.add_notification(notification)


    def initialise_admins(self):
        """! Initialise the list of admin objects from a file.
        """
        admins_data = Admin.read_from_file(ADMIN_FILENAME)
        for admin_data in admins_data:
            name = admin_data["name"]
            address = admin_data["address"]
            email = admin_data["email"]
            phone = admin_data['phone']
            username = admin_data["username"]
            password = admin_data["password"]  
            admin_object = Admin(name, address, email, phone, username, password)
            self.add_admin(admin_object)


    def initialise_staffs(self):
        """! Initialise the list of admin objects from a file.
        """
        staffs_data = FrontDeskStaff.read_from_file(FRONT_DESK_STAFF_FILENAME)
        for staff_data in staffs_data:
            name = staff_data["name"]
            address = staff_data["address"]
            email = staff_data["email"]
            phone = staff_data['phone']
            username = staff_data["username"]
            password = staff_data["password"]  
            staff_object = FrontDeskStaff(name, address, email, phone, username, password)
            self.add_front_desk_staff(staff_object)


    def initialise_customers(self):
        """! Initialise the list of customer objects from a file.
        """
        customers_data = Customer.read_customers_from_file()
        for cus_data in customers_data:
            name = cus_data["name"]
            address = cus_data["address"]
            email = cus_data["email"]
            phone = cus_data['phone']
            username = cus_data["username"]
            password = cus_data["password"]  
            customer_object = Customer(name, address, email, phone, username, password)
            self.add_customer(customer_object)


    def initialise_halls(self):
        """! Initialise the list of cinema hall objects from a file.
        """
        halls_data = CinemaHall.read_from_file(HALL_FILENAME)
        for hall_data in halls_data:
            hall_name = hall_data["hall_name"]
            capacity = hall_data["hall_capacity"]
            hall_object = CinemaHall(hall_name, capacity)
            self.__halls.append(hall_object)


    def load_database(self):
        """! Load data from various sources to initialise the system's database.
        """
        self.initialise_admins()
        self.initialise_customers()
        self.initialise_staffs()
        self.initialise_halls()
        self.initialise_movies()
        self.initialise_screenings()
        self.initialise_coupons()
        self.initialise_payments()
        self.initialise_bookings()
        self.initialise_notifications()