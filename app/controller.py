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
    

    def save_new_bookings_to_json(self, booking):
        self.cinema_data_model.save_new_bookings_to_json(booking)

    
    def add_booking_to_customer(self):
        all_customers = self.all_customers
        bookings = Booking.read_bookings_from_json_file()
        for booking in bookings:
            for customer in all_customers:
                if booking.customer == customer:
                    customer.add_booking(booking)


    def create_booking_objects_and_add_to_customer(self, username):
        bookings_info = Booking.read_bookings_from_file()
        for booking_info in bookings_info:
            if booking_info["customer_username"] == username:
                # find customer
                customer = self.find_customer(booking_info["customer_username"])

                # Convert the movie_id from string to integer
                movie_id = int(booking_info["movie_id"])
                movie = self.find_movie(movie_id)

                screening_id = int(booking_info["screening_id"])
                screening = movie.find_screening(screening_id)
                print(f'ddddddddddebug{screening}')
                if screening is None:
                    print(f"screening with ID {screening_id} not found.")

                num_of_seats = booking_info["num_of_seats"]
                selected_seats_id_list = booking_info["selected_seats"]
                print(f'ddddddddddebug{selected_seats_id_list}')
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
                payment_id = booking_info["payment_id"]
                if payment_id:
                    payment = self.find_payment(int(payment_id))
                    print(f'payment id found??????{payment}')
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
                    payment=payment)
                customer.add_booking(booking)
                

    def update_booking_payment_and_status(self, booking_id, payment_id, new_status):
        Booking.update_payment_and_status(booking_id, payment_id, new_status)


    def update_status_to_canceled(self, booking_id, new_status):
        Booking.update_status_to_canceled(booking_id, new_status)

        
    def save_new_screening_to_json(self, new_screening):
        Screening.save_new_screening_to_json(new_screening)


    def add_notifications_to_customer(self):
        filename = f'app/database/notifications.json'
        all_customers = self.all_customers
        self.cinema_data_model.retrieve_notifications_from_json(filename)
        for notification in self.cinema_data_model.notifications:
            for customer in all_customers:
                if notification.customer == customer:
                    customer.add_notification(notification)


    def save_new_screening_to_json(self, new_screening):
        self.cinema_data_model.save_new_screening_to_json(new_screening)


    def create_payment_objects_and_add_to_payments_list(self):
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


    def create_movie_objects_and_add_to_movies_list(self):
        movies_data = Movie.add_movies_from_json()
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


    def cancel_movie(self, movie_id):
        # Find the movie by its ID in the movies list
        movie_to_cancel = None
        for movie in self.all_movies:
            if movie.id == movie_id:
                movie_to_cancel = movie
                break

        if movie_to_cancel:
            # Remove the movie from the movies list
            self.all_movies.remove(movie_to_cancel)

            # Update the JSON file to remove the canceled movie
            Movie.update_movies_json(self.all_movies)


    def add_screening_to_movie(self):
        screening_data_list = Screening.read_screening_data_from_file()
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



    def save_notification_to_json(self, customer, notification):
        self.cinema_data_model.save_notification_to_json(customer, notification)


    def create_notification_objects_and_add_to_customer(self, username):
        notification_data = Notification.read_notifications_from_file()
        for data in notification_data:
            if data["customer_username"] == username:
                date_time = datetime.strptime(data["date_time"], '%Y-%m-%d %H:%M:%S.%f')
                booking_id = data["booking_id"]

                # Find the customer by username
                customer = self.find_customer(username)

                if customer is None:
                    print(f"Customer with username {username} not found.")
                    continue

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

        self.create_movie_objects_and_add_to_movies_list()

        self.add_screening_to_movie()

        self.cinema_data_model.read_coupons_from_json('app/database/coupons.json')

        for coupon in self.cinema_data_model.coupons:
            self.add_coupon(coupon)

        self.create_payment_objects_and_add_to_payments_list()
        
        for customer in self.all_customers:
            self.create_booking_objects_and_add_to_customer(customer.username)

        for customer in self.all_customers:
            self.create_notification_objects_and_add_to_customer(customer.username)