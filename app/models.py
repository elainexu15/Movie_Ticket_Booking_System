from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import List, Optional, Union
import json
import os


PAYMENT_FILENAME = 'app/database/payments.json'
NOTIFICATION_FILENAME = "app/database/notifications.json"
BOOKINGS_FILENAME = "app/database/bookings.json"
MOVIES_FILENAME = "app/database/movies.json"
SCREENINGS_FILENAME = "app/database/screenings.json"
PAYMENTS_FILENAME = "app/database/payments.json"



class General(ABC):
    @abstractmethod
    def search_movie_title(self, title: str):
        pass

    @abstractmethod
    def search_movie_lang(self, lang: str):
        pass

    @abstractmethod
    def search_movie_genre(self, genre: str):
        pass

    @abstractmethod
    def search_movie_date(self, release_date: date):
        pass

    @abstractmethod
    def view_movie_details(self, a_movie):
        pass


class Guest(General):
    def register(self):
        # Implement guest registration logic here
        pass

    def search_movie_title(self, title: str, movies):
        # Implement search by movie title for guests
        matching_movies = []

        for movie in movies:  # Assuming you have a list of movies in the General class
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)

        return matching_movies
    

    def search_movie_lang(self, selected_language: str, filtered_movies):
        # Implement search by movie language for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_language.lower() in movie.language.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        # Implement search by movie genre for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_genre.lower() in movie.genre.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        # Implement search by movie release date for guests
        matching_movies = []   
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if movie.release_date >= date_from and movie.release_date <= date_to:
                matching_movies.append(movie)
        return matching_movies


    def view_movie_details(self, a_movie):
        # Implement viewing movie details for guests
        pass

class Person(General, ABC):
    def __init__(self, name: str, address: str, email: str, phone: str) -> None:
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone

    @abstractmethod
    def search_movie_title(self, title: str):
        pass

    @abstractmethod
    def search_movie_lang(self, lang: str):
        pass

    @abstractmethod
    def search_movie_genre(self, genre: str):
        pass

    @abstractmethod
    def search_movie_date(self, release_date: date):
        pass

    @abstractmethod
    def view_movie_details(self, a_movie):
        pass


class User(Person, ABC):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password

    @abstractmethod
    def search_movie_title(self, title: str):
        pass

    @abstractmethod
    def search_movie_lang(self, lang: str):
        pass

    @abstractmethod
    def search_movie_genre(self, genre: str):
        pass

    @abstractmethod
    def search_movie_date(self, release_date: date):
        pass

    @abstractmethod
    def view_movie_details(self, a_movie):
        pass

class Admin(User):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone, username, password)

    # get admin name
    @property
    def name(self):
        return self._name

    # get admin username
    @property
    def username(self):
        return self._username
    
    # get admin password
    @property
    def password(self):
        return self._password
    
    def search_movie_title(self, title: str, movies):
        # Implement search by movie title for guests
        matching_movies = []

        for movie in movies:  # Assuming you have a list of movies in the General class
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)

        return matching_movies
    

    def search_movie_lang(self, selected_language: str, filtered_movies):
        # Implement search by movie language for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_language.lower() in movie.language.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        # Implement search by movie genre for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_genre.lower() in movie.genre.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        # Implement search by movie release date for guests
        matching_movies = []   
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if movie.release_date >= date_from and movie.release_date <= date_to:
                matching_movies.append(movie)
        return matching_movies


    def view_movie_details(self, a_movie):
        # Implement viewing movie details for guests
        pass
    

class FrontDeskStaff(User):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone, username, password)
    
    # get front desk staff name
    @property
    def name(self):
        return self._name

    # get front desk staff username
    @property
    def username(self):
        return self._username
    
    # get front desk staff password
    @property
    def password(self):
        return self._password
    
    def search_movie_title(self, title: str, movies):
        # Implement search by movie title for guests
        matching_movies = []

        for movie in movies:  # Assuming you have a list of movies in the General class
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)

        return matching_movies
    

    def search_movie_lang(self, selected_language: str, filtered_movies):
        # Implement search by movie language for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_language.lower() in movie.language.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        # Implement search by movie genre for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_genre.lower() in movie.genre.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        # Implement search by movie release date for guests
        matching_movies = []   
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if movie.release_date >= date_from and movie.release_date <= date_to:
                matching_movies.append(movie)
        return matching_movies


    def view_movie_details(self, a_movie):
        # Implement viewing movie details for guests
        pass

class Customer(User):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone, username, password)
        self.__bookings = []
        self.__notifications = []

    # get customer name
    @property
    def name(self):
        return self._name
    
    # get customer address
    @property
    def address(self):
        return self._address
    
    # get customer email
    @property
    def email(self):
        return self._email
    
    # get customer phone
    @property
    def phone(self):
        return self._phone
    
    # get customer username
    @property
    def username(self):
        return self._username
    
    # get customer password
    @property
    def password(self):
        return self._password
    
    @property
    def notifications(self):
        return self.__notifications
    
    def bookings(self):
        return self.__bookings

    def add_booking(self, new_booking):
        # Iterate through existing bookings
        for booking in self.bookings():
            if new_booking.movie.title == booking.movie.title and new_booking.screening == booking.screening and booking.status == 'Pending':
                print('You have already booked this screening. Please cancel your previous booking before proceeding.')
                return False

        # If no duplicate booking is found, add the new booking
        self.__bookings.append(new_booking)
        return True
    
    def add_notification(self, notification):
        self.__notifications.append(notification)
        
    def find_booking(self, booking_id):
        for booking in self.bookings():
            if int(booking_id) == booking.booking_id:
                return booking
        else:
            return None

    def cancel_booking(self, booking_id):
        for booking in self.bookings():
            if int(booking_id) == booking.booking_id:
                booking.status = 'Canceled'
        

    def search_movie_title(self, title: str, movies):
        # Implement search by movie title for guests
        matching_movies = []

        for movie in movies:  # Assuming you have a list of movies in the General class
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)

        return matching_movies
    

    def search_movie_lang(self, selected_language: str, filtered_movies):
        # Implement search by movie language for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_language.lower() in movie.language.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        # Implement search by movie genre for guests
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_genre.lower() in movie.genre.lower():
                matching_movies.append(movie)

        return matching_movies


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        # Implement search by movie release date for guests
        matching_movies = []   
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if movie.release_date >= date_from and movie.release_date <= date_to:
                matching_movies.append(movie)
        return matching_movies

    def view_movie_details(self, a_movie):
        # Implement viewing movie details for guests
        pass

    def to_dict(self):
        customer_dict = {
            "username": self.username,
        }
        return customer_dict
    
    def __repr__(self):
        return f'<Customer: {self.name}>'
    
# ========= class Movie ==========
class Movie:
    """! The Movie class: Represents a movie with details."""
    next_id = 100

    def __init__(self, title: str, language: str, genre: str, country: str, release_date: date, duration_in_mins: int, description: str) -> None:
        """! Constructor for the Movie class.
        @param title (str): The title of the movie.
        @param language (str): The language of the movie.
        @param genre (str): The genre of the movie.
        @param country (str): The country of the movie.
        @param release_date (date): The release date of the movie.
        @param duration_in_mins (int): The duration of the movie in minutes.
        @param description (str): A description of the movie.
        """
        self.__id = Movie.next_id    # Unique movie ID
        self.__title = title               # The title of the movie
        self.__language = language         # The language of the movie
        self.__genre = genre               # The genre of the movie
        self.__country = country           # The country of the movie
        self.__release_date = release_date # The release date of the movie
        self.__duration_in_mins = duration_in_mins  # Duration of the movie in minutes
        self.__description = description   # A description of the movie
        self.__screenings = []             # List of screenings for this movie
        Movie.next_id += 1                 # Increment the movie ID counter

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def language(self):
        return self.__language

    @property
    def genre(self):
        return self.__genre

    @property
    def country(self):
        return self.__country

    @property
    def release_date(self):
        return self.__release_date

    @property
    def duration_in_mins(self):
        return self.__duration_in_mins

    @property
    def description(self):
        return self.__description
    
    @property
    def screenings(self):
        return self.__screenings
    
    def add_screening(self, screening_object):
        self.__screenings.append(screening_object)
        self.__screenings.sort(key=lambda x: x.screening_date)

        
    def find_screening(self, screening_id):
        for screening in self.screenings:
            print(f'debug{screening}')
            if screening.screening_id == int(screening_id):
                print(f"debug {screening.screening_id}")
                return screening
        return None
    
        
    def get_screening_date_list(self):
        # Get the current date
        current_date = date.today()
        
        # Create a set of unique dates that are after the current date
        unique_dates = set()
        for screening in self.screenings:
            # Assuming that screening.screening_date is in the format "YYYY-MM-DD" without a time component
            screening_date = datetime.strptime(screening.screening_date, "%Y-%m-%d").date()
            if screening_date >= current_date and screening.is_active == True:
                unique_dates.add(screening_date)

        # Convert the set back to a list
        screening_date_list = sorted(list(unique_dates))
        return screening_date_list


    # Method to read movie data from a JSON file and create Movie objects
    @classmethod
    def add_movies_from_json(cls):
        try:
            with open(MOVIES_FILENAME, 'r') as file:
                movies_data = json.load(file)
                return movies_data
        except FileNotFoundError:
            print(f"File not found: {MOVIES_FILENAME}")
            return []
        

    @classmethod
    def update_movies_json(cls, movies):
        movies_data = [{"movie_id": movie.id,
                        "title": movie.title,
                        "language": movie.language,
                        "genre": movie.genre,
                        "country": movie.country,
                        "release_date": movie.release_date,
                        "duration": movie.duration_in_mins,
                        "description": movie.description}
                       for movie in movies]

        with open(MOVIES_FILENAME, 'w') as file:
            json.dump(movies_data, file, indent=4)

    @classmethod
    def save_new_movie_to_file(self, movie):
        # Load existing movie data from movies.json if it exists
        movie_data = []
        try:
            with open('app/database/movies.json', 'r') as json_file:
                movie_data = json.load(json_file)
        except FileNotFoundError:
            print(f"Error: File not found.")

        # Append the new movie data to the existing data
        movie_data.append({
            "title": movie.title,
            "language": movie.language,
            "genre": movie.genre,
            "country": movie.country,
            "release_date": movie.release_date,
            "duration": movie.duration_in_mins,
            "description": movie.description,
            "screenings": []
        })

        # Save the updated movie data back to movies.json
        with open('app/database/movies.json', 'w') as json_file:
            json.dump(movie_data, json_file, default=str, indent=4)



    def __str__(self):
        return f"Movie ID: {self.__id}\nTitle: {self.__title}\nLanguage: {self.__language}\nGenre: {self.__genre}\nCountry: {self.__country}\nRelease Date: {self.__release_date}\nDuration (mins): {self.__duration_in_mins}\nDescription: {self.__description}"


class CinemaHallSeat:
    def __init__(self, seat_number, row_number, is_reserved, seat_price):
        self.__seat_id = str(row_number) + str(seat_number)
        self.__seat_number = seat_number
        self.__row_number = row_number
        self.__is_reserved = is_reserved
        self.__seat_price = seat_price

    @property
    def seat_id(self):
        return self.__seat_id

    @property
    def seat_number(self):
        return self.__seat_number
    
    @property
    def row_number(self):
        return self.__row_number
    
    @property
    def is_reserved(self):
        return self.__is_reserved

    @is_reserved.setter
    def is_reserved(self, value):
        self.__is_reserved = value

    @property
    def seat_price(self):
        return self.__seat_price
    
    @seat_price.setter
    def seat_price(self, price):
        self.__seat_price = price
    
    def reserve_seat(self):
        self.__is_reserved = True

    def unreserve_seat(self):
        self.__is_reserved = False

    def to_json(self):
        # Return a dictionary representation of the seat
        return {
            "seat_number": self.__seat_number,
            "row_number": self.__row_number,
            "is_reserved": self.__is_reserved,
            "seat_price": self.__seat_price,
        }

    def __str__(self):
        return f"Seat {self.seat_id} - {'Reserved' if self.is_reserved else 'Available'} - Price {self.seat_price}"


class CinemaHall:
    """! The Hall class: Represents a movie hall with a name and seating capacity."""
    def __init__(self, hall_name: str, capacity: int) -> None:
        """! Constructor for the Hall class.
        @param hall_name (str): The name of the hall.
        @param capacity (int): The seating capacity of the hall.
        """
        self.__hall_name = hall_name  # Name of the hall
        self.__capacity = capacity    # Seating capacity of the hall

    @property
    def hall_name(self):
        return self.__hall_name
    
    @property
    def capacity(self):
        return self.__capacity

    @property
    def seats(self):
        return self.__seats
    
    def __str__(self):
        return f"Cinema Hall {self.__hall_name}, Total Seats: {self.__capacity}"


class Screening:
    next_id = 100
    def __init__(self, movie_id, screening_date, start_time, end_time, hall: CinemaHall, seats, is_active=True) -> None:
        self.__screening_id = Screening.next_id
        self.__movie_id = movie_id
        self.__screening_date = screening_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__hall = hall  
        self.__seats = seats
        self.__is_active = is_active
        Screening.next_id += 1

    @property
    def screening_id(self):
        return self.__screening_id
    
    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def screening_date(self):
        return self.__screening_date
    
    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time
    
    @property
    def hall(self):
        return self.__hall
    
    @property
    def seats(self):
        return self.__seats
    
    @property
    def is_active(self):
        return self.__is_active
    
    @is_active.setter
    def is_active(self, status):
        self.__is_active = False
    
    def to_dict(self):
        return {
            "screening_id": self.screening_id,
            "movie_id": self.movie_id,
            "screening_date": self.screening_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "hall_name": self.hall.hall_name,
            "seats": [seat.to_json() for seat in self.seats],
            "is_active": self.is_active
        }


    # Method to find a seat by its row and seat number
    def find_seat_by_identifier(self, row_number, seat_number):
        # Iterate through the seats in the hall and find the seat with matching row_number and seat_number
        for seat in self.seats:
            if seat.row_number == row_number and seat.seat_number == seat_number:
                return seat  # Return the seat object if found
        return None  # Return None if the seat is not found
    
        # Method to find a seat by its row and seat number
    def find_seat_by_id(self, seat_id):
        # Iterate through the seats in the hall and find the seat with matching row_number and seat_number
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat  # Return the seat object if found
        return None  # Return None if the seat is not found
    

    @classmethod
    def save_new_screening_to_json(self, new_screening):
        try:
            if os.path.exists(SCREENINGS_FILENAME):
                # File exists, so let's read the existing data
                with open(SCREENINGS_FILENAME, 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                # File doesn't exist, create an empty list
                existing_data = []

            # Append the new screening data to the existing data
            existing_data.append(new_screening.to_dict())

            # Write the updated data back to the file
            with open(SCREENINGS_FILENAME, 'w') as json_file:
                json.dump(existing_data, json_file, default=str, indent=4)

        except Exception as e:
            print(f"An error occurred while saving the screening data: {str(e)}")


    @classmethod
    def read_screening_data_from_file(cls):
        try:
            with open(SCREENINGS_FILENAME, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {SCREENINGS_FILENAME}")
            return []


    @classmethod
    def update_screening_status_to_inactive_to_json(cls, screening_id):
        try:
            # Read the existing screening data from the file
            screening_data_list = cls.read_screening_data_from_file()

            for screening_data in screening_data_list:
                if screening_data["screening_id"] == screening_id:
                    screening_data["is_active"] = False

            # Write the updated data back to the file
            with open(SCREENINGS_FILENAME, 'w') as json_file:
                json.dump(screening_data_list, json_file, default=str, indent=4)

        except Exception as e:
            print(f"An error occurred while updating the screening status: {str(e)}")
            

    @classmethod
    def update_reserved_seats_to_json(cls, screening_id, reserved_seats_id, is_reserved):
        try:
            # Read the existing screening data from the file
            screening_data_list = cls.read_screening_data_from_file()

            for screening_data in screening_data_list:
                if screening_data["screening_id"] == screening_id:
                    # Update the seat reservation status for this screening
                    for reserved_seat_id in reserved_seats_id:
                        for seat_data in screening_data["seats"]:
                            if reserved_seat_id == str(seat_data["row_number"]) + str(seat_data["seat_number"]):
                                seat_data["is_reserved"] = is_reserved

            # Write the updated data back to the file
            with open(SCREENINGS_FILENAME, 'w') as json_file:
                json.dump(screening_data_list, json_file, default=str, indent=4)

        except Exception as e:
            print(f"An error occurred while updating the screening status: {str(e)}")


    def __str__(self):
        return f"Screening id: {self.screening_id}\n" \
               f"Start Time: {self.start_time}\n" \
               f"End Time: {self.end_time}\n" \
               f"Hall: {self.hall}\n" \


class Coupon:
    """! The Coupon class: Represents a coupon with a unique code and discount."""
    def __init__(self, coupon_code: str, discount_percentage: float, expiration_date: date) -> None:
        """! Constructor for the Coupon class.
        @param coupon_code (str): The coupon code.
        @param discount_percentage (float): The discount percentage.
        @param expiration_date (date): The expiration date of the coupon.
        """
        self.__coupon_code = coupon_code           # The coupon code
        self.__discount_percentage = discount_percentage  # The discount percentage
        self.__expiration_date = expiration_date   # The expiration date of the coupon


    @property
    def coupon_code(self) -> str:
        """! Get the coupon code.
        @return (str): The coupon code.
        """
        return self.__coupon_code
    
    @property
    def discount_percentage(self) -> float:
        """! Get the discount percentage.
        @return (float): The discount percentage.
        """
        return self.__discount_percentage

    @property
    def expiration_date(self) -> str:
        """! Get the expiration date of the coupon.
        @return (str): The expiration date (format: "YYYY-MM-DD").
        """
        return self.__expiration_date

    def is_valid(self) -> bool:
        """Check if the coupon is valid (not expired).
        Returns:
            bool: True if the coupon is valid, otherwise False.
        """
        # Get the current date
        current_date = date.today()

        # Compare the current date with the expiration date
        if self.__expiration_date >= current_date:
            return True
        else:
            return False

    def __str__(self) -> str:
        """Get a string representation of the Coupon object.
        Returns:
            str: A string containing coupon details.
        """
        coupon_info = f"Coupon Code: {self.__coupon_code}\n"
        coupon_info += f"Discount Percentage: {self.__discount_percentage}%\n"
        coupon_info += f"Expiration Date: {self.__expiration_date}"

        return coupon_info


class Payment(ABC):
    def __init__(self, payment_id: int, amount: float, created_on: datetime, coupon: Optional[Coupon]):
        self._payment_id = payment_id
        self._amount = amount
        self._created_on = created_on
        self._coupon = coupon

    @abstractmethod
    def process_payment(self):
        pass


    @classmethod
    def read_payments_from_file(cls):
        try:
            with open(PAYMENTS_FILENAME, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {PAYMENTS_FILENAME}")
            return []
        

class CreditCard(Payment):
    def __init__(self, payment_id:int, amount: float, created_on: datetime, coupon: Optional[Coupon],
                 credit_card_number: str, card_type: str, expiry_date: datetime, name_on_card: str):
        super().__init__(payment_id, amount, created_on, coupon)
        self.__credit_card_number = credit_card_number
        self.__card_type = card_type
        self.__expiry_date = expiry_date
        self.__name_on_card = name_on_card
    
    @property
    def payment_id(self):
        return self._payment_id

    @property
    def credit_card_number(self):
        return self.__credit_card_number
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def coupon(self):
        return self._coupon

    def to_dict(self):
        return {
            'payment_id': self._payment_id,
            'amount': self._amount,
            'coupon': self.coupon.coupon_code if self.coupon else None,
            'created_on': self._created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'credit_card_number': self.credit_card_number,  # Using the property method
            'card_type': self.__card_type,
            'expiry_date': self.__expiry_date,
            'name_on_card': self.__name_on_card
        }
    
    def process_payment(self):
        # In a real application, I would use a payment gateway or service (e.g., Stripe, PayPal).
        # This is a simplified example, so I'll just print a success message.
        print(f"Processing a payment using credit card ending in {self.credit_card_number[-4:]}")
        return True
    
    def process_refund(self):
        # In a real application, I would use a payment gateway or service (e.g., Stripe, PayPal).
        # This is a simplified example, so I'll just print a success message.
        print(f"Processing a refund payment using credit card ending in {self.credit_card_number[-4:]}")
        return True


    
    @classmethod
    def save_payment_to_json(cls, payment):
        if payment is None:
            return

        existing_data = []

        if os.path.exists(PAYMENT_FILENAME):
            with open(PAYMENT_FILENAME, "r") as json_file:
                existing_data = json.load(json_file)

        existing_data.append(payment.to_dict())

        with open(PAYMENT_FILENAME, "w") as json_file:
            json.dump(existing_data, json_file, default=str, indent=4)

        print(f"Payment has been saved to {PAYMENT_FILENAME}")


class DebitCard(Payment):
    def __init__(self, payment_id: int, amount: float, created_on: datetime, coupon: Optional[Coupon],
                 card_number: str, bank_name: str, name_on_card: str):
        super().__init__(payment_id, amount, created_on, coupon)
        self.__card_number = card_number
        self.__bank_name = bank_name
        self.__name_on_card = name_on_card

    def process_payment(self):
        # Add logic to process payment using a debit card
        pass


class Booking:
    next_id = 1
    def __init__(self, customer: Customer, movie: Movie, screening: Screening, num_of_seats: int, selected_seats: List[CinemaHallSeat], created_on: date, total_amount: float, status: str, payment = None, coupon = None) -> None:
        self.__booking_id = Booking.next_id
        self.__customer = customer
        self.__movie = movie
        self.__screening = screening
        self.__num_of_seats = num_of_seats
        self.__selected_seats = selected_seats
        self.__created_on = created_on
        self.__total_amount = total_amount
        self.__status = status
        self.__payment = payment
        self.__coupon = coupon
        Booking.next_id += 1
    
    @property
    def booking_id(self):
        return self.__booking_id
    
    @property
    def customer(self):
        return self.__customer

    @property
    def movie(self):
        return self.__movie
    
    @property
    def screening(self):
        return self.__screening
    
    @property
    def num_of_seats(self):
        return self.__num_of_seats

    @property
    def selected_seats(self):
        return self.__selected_seats
    
    @property
    def created_on(self):
        return self.__created_on
    
    @property
    def total_amount(self):
        return self.__total_amount
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, status):
        self.__status = status
    
    @property
    def coupon(self):
        return self.__coupon
    
    @coupon.setter
    def coupon(self, coupon):
        self.__coupon = coupon

    @total_amount.setter
    def total_amount(self, total_amount):
        self.__total_amount = total_amount

    @property
    def payment(self):
        return self.__payment

    @payment.setter
    def payment(self, apayment):
        self.__payment = apayment

    def add_payment(self, payment):
        self.__payment = payment

    def to_dict(self):
        booking_dict = {
            "booking_id": self.__booking_id,
            "customer_username": self.__customer.username,
            "movie_id": self.__movie.id,
            "screening_id": self.__screening.screening_id,
            "num_of_seats": self.__num_of_seats,
            "selected_seats": [seat.seat_id for seat in self.__selected_seats],
            "created_on": self.__created_on.isoformat(),
            "total_amount": self.__total_amount,
            "payment_id": self.__payment.payment_id if self.__payment else None,
            "status": self.__status,
        }
        if self.__payment:
            booking_dict["payment"] = self.__payment.payment_id
        if self.__coupon:
            booking_dict["coupon"] = self.__coupon.coupon_code
        return booking_dict


    @classmethod
    def read_bookings_from_file(cls):
        try:
            with open(BOOKINGS_FILENAME, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {BOOKINGS_FILENAME}")
            return []


    @classmethod
    def update_payment_and_status(cls, booking_id, payment_id, new_status):
        bookings_info = cls.read_bookings_from_file()

        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                booking_info["payment_id"] = payment_id
                booking_info["status"] = new_status

        cls.save_bookings_to_file(bookings_info)


    @classmethod
    def update_status_to_canceled(cls, booking_id, new_status):
        bookings_info = cls.read_bookings_from_file()
        print(f"allllllll booking info {bookings_info}")
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                print(booking_info["status"])
                booking_info["status"] = new_status
                print(booking_info["status"])

        cls.save_bookings_to_file(bookings_info)


    @classmethod
    def update_status_to_refund(cls, booking_id, new_status):
        bookings_info = cls.read_bookings_from_file()
        print(f"allllllll booking info {bookings_info}")
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                print(booking_info["status"])
                booking_info["status"] = new_status
                print(booking_info["status"])

        cls.save_bookings_to_file(bookings_info)


    @classmethod
    def save_bookings_to_file(cls, bookings_info):
        with open(BOOKINGS_FILENAME, 'w') as file:
            json.dump(bookings_info, file, indent=4)



    def __str__(self):
        return f"Booking ID: {self.__booking_id}\n" \
               f"Customer: {self.__customer}\n" \
               f"Screening: {self.__screening}\n" \
               f"Number of Seats: {self.__num_of_seats}\n" \
               f"Selected Seats: {', '.join(map(str, self.__selected_seats))}\n" \
               f"Created On: {self.__created_on}\n" \
               f"Total Amount: {self.__total_amount}\n" \
               f"Payment: {self.__payment}\n" \
               f"Status: {self.__status}"
    


class Notification:
    """! The Notification class: Represents a notification sent to a user. """
    next_id = 100
    def __init__(self, customer, subject: str, message: str, date_time: datetime,  booking: Booking = None) -> None:
        """! Constructor for the Notification class.
        @param message (str): The message content of the notification.
        @param date_time (datetime): The date and time when the notification is sent.
        @param subject (str): The subject of the notification.
        @param booking (Booking): The associated booking (optional).
        @param payment (Payment): The associated payment (optional).
        """
        self.__notification_id = Notification.next_id
        self.__customer = customer
        self.__message = message
        self.__date_time = date_time
        self.__subject = subject
        self.__booking = booking
        Notification.next_id += 1

    @property
    def notification_id(self):
        return self.__notification_id
    
    @property
    def customer(self):
        return self.__customer
    
    @property
    def subject(self):
        return self.__subject
    
    @property
    def message(self):
        return self.__message
    
    @property
    def date_time(self):
        return self.__date_time
    
    @property
    def booking(self):
        return self.__booking

    @classmethod
    def save_notification_to_json(self, notification):
        if notification is None:
            return

        existing_data = []

        if os.path.exists(NOTIFICATION_FILENAME):
            # File exists, so let's read the existing data
            with open(NOTIFICATION_FILENAME, "r") as json_file:
                existing_data = json.load(json_file)

        # Format date_time to include only three decimal places
        date_time_formatted = notification.date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # Append the new notification to the existing data
        existing_data.append({
            "notification_id": notification.notification_id,
            "customer_username": notification.customer.username,
            "subject": notification.subject,
            "message": notification.message,
            "date_time": date_time_formatted,
            "booking_id": notification.booking.booking_id if notification.booking else None
        })

        # Write the updated data back to the file
        with open(NOTIFICATION_FILENAME, "w") as json_file:
            json.dump(existing_data, json_file, default=str, indent=4)

        print(f"Notification for {notification.customer.username} has been saved")


    @classmethod
    def read_notifications_from_file(cls):
        try:
            with open(NOTIFICATION_FILENAME, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {NOTIFICATION_FILENAME}")
            return []

    
class CinemaDataModel():
    def __init__(self):
        self.__customers = []
        self.__admins = []
        self.__front_desk_staffs = []
        self.__movies = []
        self.__halls = []
        self.__coupons = []
        self.__payments = []
        self.__screenings = []
        self.__bookings = []
        self.__notifications = []

    @property
    def admins(self):
        return self.__admins
    
    @property
    def customers(self):
        return self.__customers
    
    @property
    def front_desk_staffs(self):
        return self.__front_desk_staffs
    
    @property
    def movies(self):
        return self.__movies
    
    @property
    def halls(self):
        return self.__halls
    
    @property
    def screenings(self):
        return self.__screenings
    
    @property
    def bookings(self):
        return self.__bookings
    
    @property
    def payments(self):
        return self.__payments
    
    @property
    def notifications(self):
        return self.__notifications
    
    def add_payment(self, a_payment):
        self.__payments.append(a_payment)

    def find_movie(self, id):
        for movie in self.movies:
            if movie.id == id:
                return movie
        return None
    

    def find_hall(self, hall_name):
        for hall in self.halls:
            if hall.hall_name == hall_name:
                return hall
        return None


    def find_customer(self, username):
        for customer in self.__customers:
            if customer.username == username:
                return customer
        return None
    
    def find_payment(self, new_payment_id):
        for payment in self.payments:
            if payment.payment_id == new_payment_id:
                return payment
        return None
    
    def find_coupon(self, coupon_code):
        for coupon in self.all_coupons:
            if coupon.coupon_code == coupon_code:
                return coupon 
        return None

    @property
    def coupons(self):
        return self.__coupons

    def handle_json_file_errors(self, file_name):
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r') as json_file:
                    return json.load(json_file)
            else:
                print(f"Error: File '{file_name}' not found.")
                return None
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")
            return None



    def handle_txt_file_errors(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")
        return []
        
    def add_admins_from_file(self, file_name):
        lines = self.handle_txt_file_errors(file_name)
        for line in lines:
            data = line.strip().split(',')
            name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
            admin_object = Admin(name, address, email, phone, username, password)
            self.__admins.append(admin_object)


    def add_front_desk_staffs_from_file(self, file_name):
        lines = self.handle_txt_file_errors(file_name)
        for line in lines:
            data = line.strip().split(',')
            name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
            front_desk_staff_object = FrontDeskStaff(name, address, email, phone, username, password)
            self.__front_desk_staffs.append(front_desk_staff_object)


    # Method to read customer data from a file and create Customer objects
    def add_customers_from_file(self, file_name):
        lines = self.handle_txt_file_errors(file_name)
        for line in lines:
            data = line.strip().split(',')
            name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
            customer_object = Customer(name, address, email, phone, username, password)
            self.__customers.append(customer_object)

    # Method to read hall data from a file and create Cinema Hall objects
    def add_hall_from_file(self, file_name):
        lines = self.handle_txt_file_errors(file_name)
        for line in lines:
            data = line.strip().split(',')
            hall_name, capacity = data[0], int(data[1])
            cinema_hall_object = CinemaHall(hall_name, capacity)
            self.__halls.append(cinema_hall_object)

    
    # Initialize seats for the screening
    def initialise_seats(self, hall, price):  
        seats = []    
        for row_number in range(1, hall.capacity // 10 + 1):  # Assuming 10 seats per row
            for seat_number in range(1, 11):  # 10 seats per row
                seat = CinemaHallSeat(seat_number, row_number, False, price)  # Initialize seats
                seats.append(seat)
        return seats




    def read_coupons_from_json(self, json_file):        
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                for item in data:
                    coupon_code = item.get('coupon_code', '')
                    discount = item.get('discount_percentage', 0.0)
                    expiry_date_str = item.get('expiration_date', '')
                    # Parse the date string into a datetime object
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
                    
                    # Create a Coupon object and add it to the list
                    coupon = Coupon(coupon_code, discount, expiry_date)
                    self.__coupons.append(coupon)
        
        except FileNotFoundError:
            print(f"File '{json_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{json_file}'.")



 
    
    def save_new_bookings_to_json(self, booking):
        filename = f"app/database/bookings.json"
        existing_data = []

        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            # File exists and is not empty, so let's read the existing data
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)

        # Append the new screening data to the existing data
        existing_data.append(booking.to_dict())

        # Write the updated data back to the file
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, default=str, indent=4)



    def save_new_screening_to_json(self, new_screening):
        # Define the filename based on the movie ID
        filename = 'app/database/screenings.json'

        try:
            if os.path.exists(filename):
                # File exists, so let's read the existing data
                with open(filename, 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                # File doesn't exist, create an empty list
                existing_data = []

            # Append the new screening data to the existing data
            existing_data.append(new_screening.to_dict())

            # Write the updated data back to the file
            with open(filename, 'w') as json_file:
                json.dump(existing_data, json_file, default=str, indent=4)

            return True  # Successfully saved

        except Exception as e:
            print(f"An error occurred while saving the screening data: {str(e)}")
            return False  # Failed to save

