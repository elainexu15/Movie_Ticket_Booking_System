from .models import *
import json
import os


class CinemaController:
    def __init__(self):
        self.__cinema_data_model = CinemaDataModel()
        self.__customers = []
        self.__admins = []
        self.__front_desk_staffs = []
        self.__movies = []
        self.__halls = []
        self.__coupons = []
        self.__payments = []
    
    @property
    def cinema_data_model(self):
        return self.__cinema_data_model

    @property
    def all_customers(self):
        return self.__customers
    
    @property
    def all_admins(self):
        return self.__admins

    @property
    def all_front_desk_staffs(self):
        return self.__front_desk_staffs

    @property
    def all_movies(self):
        return self.__movies
    
    @property
    def all_halls(self):
        return self.__halls
    
    @property
    def all_coupons(self):
        return self.__coupons
    
    @property
    def all_payments(self):
        return self.__payments

    def find_customer(self, username):
        for customer in self.__customers:
            if customer.username == username:
                return customer
        return None

    def find_movie(self, id):
        for movie in self.__movies:
            if movie.id == id:
                return movie
        return None
    
    def find_hall(self, hall_name):
        for hall in self.__halls:
            if hall.hall_name == hall_name:
                return hall
        return None
    
    def find_coupon(self, coupon_code):
        for coupon in self.all_coupons:
            if coupon.coupon_code == coupon_code:
                return coupon 
        return None

    def find_payment(self, new_payment_id):
        for payment in self.all_payments:
            if payment.payment_id == new_payment_id:
                return payment
        return None


    def add_customer(self, customer):
        self.__customers.append(customer)
    
    def add_admin(self, admin):
        self.__admins.append(admin)

    def add_front_desk_staff(self, front_desk_staff):
        self.__front_desk_staffs.append(front_desk_staff)

    def add_movie(self, movie_object):
        self.__movies.append(movie_object)

    def add_hall(self, hall_object):
        self.__halls.append(hall_object)

    def add_payment(self, a_payment):
        self.__payments.append(a_payment)
            
    def add_coupon(self, coupon):
        self.__coupons.append(coupon)

    def register_customer(self, name, address, email, phone, username, hashed_password) -> bool:
        # Check if the username already exists
        if self.find_customer(username):
            return False
        new_customer = Customer(name, address, email, phone, username, hashed_password)
        self.add_customer(new_customer)
        with open('app/database/customers.txt', 'a') as file:
            file.write(f"{new_customer.name},{new_customer.address},{new_customer.email},{new_customer.phone},{new_customer.username},{new_customer.password}\n")
        return True


    def get_language_list(self):
        language_list = []
        for movie in self.all_movies:
            if movie.language not in language_list:
                language_list.append(movie.language)
        return language_list
    
    def get_genre_list(self):
        genre_list = []
        for movie in self.all_movies:
            if movie.genre not in genre_list:
                genre_list.append(movie.genre)
        return genre_list
    

    # ======== filter movies ========
    def filter_movies(self, title, selected_language, selected_genre, date_from, date_to, guest):
        filtered_movies = self.all_movies
        if title:
            filtered_movies = guest.search_movie_title(title, filtered_movies)
        if selected_language:
            if selected_language == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = guest.search_movie_lang(selected_language, filtered_movies)
        if selected_genre:
            if selected_genre == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = guest.search_movie_genre(selected_genre, filtered_movies)
        if not date_from or not date_to:
            filtered_movies = filtered_movies
        else:
            filtered_movies = guest.search_movie_date(date_from, date_to, filtered_movies)
        return filtered_movies
    
    
    def customer_filter_movies(self, title, selected_language, selected_genre, date_from, date_to, customer):
        filtered_movies = self.all_movies
        if title:
            filtered_movies = customer.search_movie_title(title, filtered_movies)
        if selected_language:
            if selected_language == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = customer.search_movie_lang(selected_language, filtered_movies)
        if selected_genre:
            if selected_genre == 'all':
                filtered_movies = filtered_movies
            else:
                filtered_movies = customer.search_movie_genre(selected_genre, filtered_movies)
        if not date_from or not date_to:
            filtered_movies = filtered_movies
        else:
            filtered_movies = customer.search_movie_date(date_from, date_to, filtered_movies)
        return filtered_movies


    def find_screening_by_date_and_time(self, movie, screening_date, start_time):
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
    

    def validate_coupon(self, coupon_code):
        today_date = datetime.now()        
        # get valid coupon codes
        valid_coupon_codes = []  
        for coupon in self.all_coupons:
            if coupon.expiration_date.date() >= today_date.date():
                valid_coupon_codes.append(coupon.coupon_code)
        coupon = self.find_coupon(coupon_code)


    def check_seat_availability(self, booking):
        selected_seats = booking.selected_seats
        screening = booking.screening
        reserved_seats = [seat.seat_id for seat in screening.seats if seat.is_reserved == True]
    
        for selected_seat in selected_seats:
            if selected_seat.seat_id in reserved_seats:
                return False
        
        return True


    def save_reserved_seats_to_json(self, movie_id, screening_id, reserved_seats_id):
        self.cinema_data_model.save_reserved_seats_to_json(movie_id, screening_id, reserved_seats_id)


    def update_booking_payment_and_status(self, customer, booking, update_payment=False):
        self.cinema_data_model.update_booking_payment_and_status(customer, booking, update_payment=False)


    def save_new_bookings_to_json(self, booking):
        self.cinema_data_model.save_new_bookings_to_json(booking)

    
    def add_booking_to_customer(self):
        filename = f'app/database/bookings.json'
        all_customers = self.all_customers
        self.cinema_data_model.read_bookings_from_json_file(filename)
        for booking in self.cinema_data_model.bookings:
            for customer in all_customers:
                if booking.customer == customer:
                    customer.add_booking(booking)


    def save_new_screening_to_json(self, new_screening):
        self.cinema_data_model.save_new_screening_to_json(new_screening)


    def save_payment_to_json(self, payment):
        self.cinema_data_model.save_payment_to_json(payment)


    def save_new_movie_to_file(self, new_movie):
        self.cinema_data_model.save_new_movie_to_file(new_movie)


    def add_screening_to_movie(self, screenings:List):
        for screening in self.cinema_data_model.screenings:
            for movie in self.all_movies:
                if movie.id == screening.movie_id:
                    movie.add_screening(screening)


    def save_notification_to_json(self, customer, notification):
        self.cinema_data_model.save_notification_to_json(customer, notification)


    def load_database(self):

        self.cinema_data_model.add_customers_from_file('app/database/customers.txt')
        for customer in self.cinema_data_model.customers:
            self.add_customer(customer)

        self.cinema_data_model.add_admins_from_file('app/database/admins.txt')
        for admin in self.cinema_data_model.admins:
            self.add_admin(admin)

        self.cinema_data_model.add_front_desk_staffs_from_file('app/database/front_desk_staffs.txt')
        for front_desk_staff in self.cinema_data_model.front_desk_staffs:
            self.add_front_desk_staff(front_desk_staff)

        self.cinema_data_model.add_hall_from_file('app/database/cinema_hall.txt')
        for hall in self.cinema_data_model.halls:
            self.add_hall(hall)

        self.cinema_data_model.add_movies_from_json('app/database/movies.json')
        for movie in self.cinema_data_model.movies:
            self.add_movie(movie)

        self.cinema_data_model.add_screening_from_file('app/database/screenings.json')
        screenings = self.cinema_data_model.screenings
        self.add_screening_to_movie(screenings)

        self.cinema_data_model.read_coupons_from_json('app/database/coupons.json')

        for coupon in self.cinema_data_model.coupons:
            self.add_coupon(coupon)


        # read payments from json file:
        for payment in self.cinema_data_model.payments:
            self.add_payment(payment)
        

        self.add_booking_to_customer()


