from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import List, Optional, Union


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
    
    def bookings(self):
        return self.__bookings

    def add_booking(self, new_booking):
        for booking in self.bookings():
            if new_booking.movie.title == booking.movie.title and new_booking.screening == booking.screening and booking.status != 'canceled':
                return 0
                print('You have already booked this screening. please cancel your previous booking before proceed')
        self.__bookings.append(new_booking)
    
    def find_booking(self, booking_id):
        for booking in self.bookings():
            if int(booking_id) == booking.booking_id:
                return booking
        else:
            return None



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
            if screening.screening_id == screening_id:
                return screening
            else:
                return None
    
        
    def get_screening_date_list(self):
        # Get the current date
        current_date = date.today()
        
        # Create a set of unique dates that are after the current date
        unique_dates = set()
        for screening in self.screenings:
            # Assuming that screening.screening_date is in the format "YYYY-MM-DD" without a time component
            screening_date = datetime.strptime(screening.screening_date, "%Y-%m-%d").date()
            if screening_date >= current_date:
                unique_dates.add(screening_date)

        # Convert the set back to a list
        screening_date_list = sorted(list(unique_dates))
        return screening_date_list


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
    def __init__(self, screening_date, start_time, end_time, hall: CinemaHall, seats) -> None:
        self.__screening_id = Screening.next_id
        self.__screening_date = screening_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__hall = hall  
        self.__seats = seats
        Screening.next_id += 1

    @property
    def screening_id(self):
        return self.__screening_id

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
    



    def __str__(self):
        return f"Screening Date: {self.screening_date}\n" \
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
        self.__payment_id = payment_id
        self.__amount = amount
        self.__created_on = created_on
        self.__coupon = coupon

    @abstractmethod
    def process_payment(self):
        pass

class CreditCard(Payment):
    def __init__(self, payment_id: int, amount: float, created_on: datetime, coupon: Optional[Coupon],
                 credit_card_number: str, card_type: str, expiry_date: datetime, name_on_card: str):
        super().__init__(payment_id, amount, created_on, coupon)
        self.__credit_card_number = credit_card_number
        self.__card_type = card_type
        self.__expiry_date = expiry_date
        self.__name_on_card = name_on_card

    def process_payment(self):
        # Add logic to process payment using a credit card
        pass

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
        self.__coupon = None
        Booking.next_id += 1
    
    @property
    def booking_id(self):
        return self.__booking_id
    
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
    
    @property
    def coupon(self):
        return self.__coupon
    
    @coupon.setter
    def coupon(self, coupon):
        self.__coupon = coupon

    @total_amount.setter
    def total_amount(self, total_amount):
        self.__total_amount = total_amount

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
            "status": self.__status,
        }
        if self.__payment:
            booking_dict["payment"] = self.__payment.payment_id
        if self.__coupon:
            booking_dict["coupon"] = self.__coupon.coupon_code
        return booking_dict

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