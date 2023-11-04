"""! @brief Data Models"""

##
# @file models.py
#
# @brief Data Models for Cinema System
#
# @section description_controller Description
# The models.py module contains Python classes that represent key components of 
# the cinema system. These classes encapsulate the properties and behaviors 
# associated with each entity. The data models defined in this module include:
# 
# - Customer: Represents cinema customers with attributes like name, email, and password.
# - Admin: Represents administrators responsible for system management.
# - Staff: Represents staff members involved in theater operations.
# - Hall: Describes cinema halls with details such as capacity and availability.
# - Movie: Represents movie listings with attributes like title, genre, and release date.
# - Screening: Defines movie screenings, including date, time, and hall information.
# - Booking: Represents customer bookings, including selected seats and payment details.
# - Notification: Represents notifications sent to customers.
# - Coupon: Defines coupon objects for discounts on bookings.
# - Payment: Represents payment transactions for bookings.
# - These models lay the groundwork for organizing and managing data within the cinema system and facilitate interactions between different system components.
#
# @section notes_clinic Notes
# - Ensure that the attributes and methods associated with each model class are fully implemented and adhere to the requirements of the Lincoln Cinema Online Movie Ticket System.
# - Maintain consistency in data modeling and follow best practices for database design to support the system's functionality and scalability.
# - Additional methods and relationships between models may be added as the system's features are further developed and refined.
#
# @section author_cinema Author
# Created by Elaine Xu on 28/09/2023

# Imports
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
COUPON_FILENAME = "app/database/coupons.json"
HALL_FILENAME = "app/database/cinema_hall.json"
ADMIN_FILENAME = "app/database/admins.json"
CUSTOMER_FILENAME = "app/database/customers.json"
FRONT_DESK_STAFF_FILENAME = "app/database/front_desk_staffs.json"


class Base:
    """The Base class defines common methods and properties for searching and file I/O operations."""
    @classmethod
    def read_from_file(cls, filename):
        """Read data from a file and return it."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []

    @classmethod
    def save_to_file(cls, data, filename):
        """Save data to a file in JSON format."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def search_movie_title(self, title: str, movies):
        """! Search for movies by title.
        @param title (str): The title of the movie to search for.
        @param movies: List of movies to search in.
        @return: List of matching movies.
        """
        matching_movies = []
        for movie in movies:  # Assuming you have a list of movies in the General class
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)
        return matching_movies
    

    @classmethod
    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Search for movies by language.
        @param selected_language (str): The selected language to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        matching_movies = []

        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_language.lower() in movie.language.lower():
                matching_movies.append(movie)

        return matching_movies

    @classmethod
    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Search for movies by genre.
        @param selected_genre (str): The selected genre to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        matching_movies = []
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if selected_genre.lower() in movie.genre.lower():
                matching_movies.append(movie)

        return matching_movies

    @classmethod
    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Search for movies by release date.
        @param date_from (date): The starting date for the search.
        @param date_to (date): The ending date for the search.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        matching_movies = []   
        for movie in filtered_movies:  # Assuming you have a list of movies in the General class
            if movie.release_date>= date_from and movie.release_date <= date_to:
                matching_movies.append(movie)
        return matching_movies


class General(ABC, Base):
    """! The General class is an abstract base class that defines methods for searching and viewing movie details."""

    @abstractmethod
    def search_movie_title(self, title: str):
        """! Abstractmethod method for searching for movies by title for guest users."""
        pass
        
    @abstractmethod
    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Abstractmethod method for searching for movies by language for guest users."""
        pass

    @abstractmethod
    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Abstractmethod method for searching for movies by genre for guest users."""
        pass

    @abstractmethod
    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Abstractmethod method for searching for movies by date for guest users."""
        pass


class Guest(General, Base):
    """! The Guest class extends the General class and implements guest-specific movie search and registration logic."""

    @classmethod
    def register(cls, name, address, email, phone, username, hashed_password):
        """Register a new customer and store their information.
        @param name: The customer's name.
        @param address: The customer's address.
        @param email: The customer's email address.
        @param phone: The customer's phone number.
        @param username: The desired username for the customer.
        @param hashed_password: The hashed password for the customer.
        @return: Customer object
        """
        # Create a new customer object
        customer = Customer(name, address, email, phone, username, hashed_password)
        existing_data = cls.read_from_file(CUSTOMER_FILENAME)

        # Append the new customer data to the existing data
        existing_data.append(customer.to_dict())

        # Write the updated data back to the file
        cls.save_to_file(existing_data, CUSTOMER_FILENAME)

        return customer

   
    def search_movie_title(self, title: str, movies):
        """! Search for movies by title for guest users.
        @param title (str): The title of the movie to search for.
        @param movies: List of movies to search in.
        @return: List of matching movies.
        """
        return Base.search_movie_title(title, movies)


    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Search for movies by language for guest users.
        @param selected_language (str): The selected language to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_lang(selected_language, filtered_movies)


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Search for movies by genre for guest users.
        @param selected_genre (str): The selected genre to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_genre(selected_genre, filtered_movies)


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Search for movies by release date for guest users.
        @param date_from (date): The starting date for the search.
        @param date_to (date): The ending date for the search.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_date(date_from,date_to, filtered_movies)


class Person(General, ABC):
    """! The Person class extends the General class and represents a person with a name, address, email, and phone."""

    def __init__(self, name: str, address: str, email: str, phone: str) -> None:
        """! Constructor for the Person class.
        @param name (str): The name of the person.
        @param address (str): The address of the person.
        @param email (str): The email address of the person.
        @param phone (str): The phone number of the person.
        """
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone

    @abstractmethod
    def search_movie_title(self, title: str):
        """! Abstractmethod method for searching for movies by title for guest users."""
        pass
        
    @abstractmethod
    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Abstractmethod method for searching for movies by language for guest users."""
        pass

    @abstractmethod
    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Abstractmethod method for searching for movies by genre for guest users."""
        pass

    @abstractmethod
    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Abstractmethod method for searching for movies by date for guest users."""
        pass


class User(Person, ABC):
    """! The User class extends the Person class and represents a user with a username and password."""
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        """! Constructor for the User class.
        @param name (str): The name of the user.
        @param address (str): The address of the user.
        @param email (str): The email address of the user.
        @param phone (str): The phone number of the user.
        @param username (str): The username for user authentication.
        @param password (str): The password for user authentication.
        """
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password

    @abstractmethod
    def search_movie_title(self, title: str):
        """! Abstractmethod method for searching for movies by title for guest users."""
        pass
        
    @abstractmethod
    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Abstractmethod method for searching for movies by language for guest users."""
        pass

    @abstractmethod
    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Abstractmethod method for searching for movies by genre for guest users."""
        pass

    @abstractmethod
    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Abstractmethod method for searching for movies by date for guest users."""
        pass


class Admin(User, Base):
    """! The Admin class extends the User class and represents an administrator with privileges to manage system features."""
    """! Constructor for the Admin class.
        @param name (str): The name of the administrator.
        @param address (str): The address of the administrator.
        @param email (str): The email address of the administrator.
        @param phone (str): The phone number of the administrator.
        @param username (str): The username for administrator authentication.
        @param password (str): The password for administrator authentication.
        """
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone, username, password)

    @property
    def name(self):
        """! Get the name of the administrator.
        @return (str): The name of the administrator.
        """
        return self._name

    @property
    def username(self):
        """! Get the username of the administrator.
        @return (str): The username for administrator authentication.
        """
        return self._username
    
    @property
    def password(self):
        """! Get the password of the administrator.
        @return (str): The password for administrator authentication.
        """
        return self._password
    
    @classmethod
    def read_admins_from_file(cls):
        """
        ! Read admin data from a file and create Admin objects.
        @return (str): A list of admin objects.
        """
        admins_data = cls.read_from_file(ADMIN_FILENAME)
        return admins_data


    @classmethod
    def cancel_booking(cls, booking_id, new_status):
        """! Cancel a booking by its ID and update its status.
        @param booking_id (str): The ID of the booking to cancel.
        @param new_status (str): The new status to set for the booking.
        """
        bookings_info = cls.read_from_file(BOOKINGS_FILENAME)
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                booking_info["status"] = new_status

        cls.save_to_file(bookings_info, BOOKINGS_FILENAME)

    
    def search_movie_title(self, title: str, movies):
        """! Search for movies by title for guest users.
        @param title (str): The title of the movie to search for.
        @param movies: List of movies to search in.
        @return: List of matching movies.
        """
        return Base.search_movie_title(title, movies)


    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Search for movies by language for guest users.
        @param selected_language (str): The selected language to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_lang(selected_language, filtered_movies)


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Search for movies by genre for guest users.
        @param selected_genre (str): The selected genre to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_genre(selected_genre, filtered_movies)


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Search for movies by release date for guest users.
        @param date_from (date): The starting date for the search.
        @param date_to (date): The ending date for the search.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_date(date_from, date_to, filtered_movies)
    

class FrontDeskStaff(User, Base):
    """! The FrontDeskStaff class extends the User class and represents front desk staff with specific privileges.
    """
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        """! Constructor for the FrontDeskStaff class.
        @param name (str): The name of the front desk staff.
        @param address (str): The address of the front desk staff.
        @param email (str): The email address of the front desk staff.
        @param phone (str): The phone number of the front desk staff.
        @param username (str): The username for authentication.
        @param password (str): The password for authentication.
        """
        super().__init__(name, address, email, phone, username, password)
    

    @property
    def name(self):
        """! Get the name of the FrontDeskStaff.
        @return (str): The name of the FrontDeskStaff."""
        return self._name


    @property
    def username(self):
        """! Get the username of the FrontDeskStaff.
        @return (str): The username of the FrontDeskStaff."""
        return self._username
    

    @property
    def password(self):
        """! Get the password of the FrontDeskStaff.
        @return (str): The password of the FrontDeskStaff."""
        return self._password 


    @classmethod
    def cancel_booking(cls, booking_id, new_status):
        """! Cancel a booking by updating its status.
        @param booking_id (str): The ID of the booking to cancel.
        @param new_status (str): The new status for the booking.
        """
        bookings_info = cls.read_from_file(BOOKINGS_FILENAME)
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                booking_info["status"] = new_status

        cls.save_to_file(bookings_info, BOOKINGS_FILENAME)


    @classmethod
    def save_bookings_to_file(cls, bookings_info):
        """! Save booking information to a file.
        @param bookings_info (List[Dict]): A list of booking information to save.
        """
        with open(BOOKINGS_FILENAME, 'w') as file:
            json.dump(bookings_info, file, indent=4)


    @classmethod
    def add_front_desk_staffs_from_file(cls):
        """! Read front desk staff data from a file and create FrontDeskStaff objects.
        @return (List[FrontDeskStaff]): A list of FrontDeskStaff objects.
        """
        staffs_data = cls.read_from_file(FRONT_DESK_STAFF_FILENAME)
        return staffs_data
    

    def search_movie_title(self, title: str, movies):
        """! Search for movies by title for guest users.
        @param title (str): The title of the movie to search for.
        @param movies: List of movies to search in.
        @return: List of matching movies.
        """
        return Base.search_movie_title(title, movies)


    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Search for movies by language for guest users.
        @param selected_language (str): The selected language to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_lang(selected_language, filtered_movies)


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Search for movies by genre for guest users.
        @param selected_genre (str): The selected genre to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_genre(selected_genre, filtered_movies)


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Search for movies by release date for guest users.
        @param date_from (date): The starting date for the search.
        @param date_to (date): The ending date for the search.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_date(date_from,date_to, filtered_movies)


class Customer(User, Base):
    """! The Customer class extends the User class and represents a customer with booking and notification features.
    """
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        """! Constructor for the Customer class.
        @param name (str): The name of the customer.
        @param address (str): The address of the customer.
        @param email (str): The email address of the customer.
        @param phone (str): The phone number of the customer.
        @param username (str): The username for authentication.
        @param password (str): The password for authentication.
        """
        super().__init__(name, address, email, phone, username, password)
        self.__bookings = []
        self.__notifications = []

    @property
    def name(self):
        """! Get the name of the customer.
        @return (str): The name of the customer."""
        return self._name   

    @property
    def username(self):
        """! Get the username of the customer.
        @return (str): The username of the customer."""
        return self._username
    
    @property
    def address(self):
        """! Get the address of the customer.
        @return (str): The address of the customer."""
        return self._address
    
    @property
    def phone(self):
        """! Get the phone of the customer.
        @return (str): The phone of the customer."""
        return self._phone
    
    @property
    def email(self):
        """! Get the email of the customer.
        @return (str): The email of the customer."""
        return self._email
    
    @property
    def password(self):
        """! Get the password of the customer.
        @return (str): The password of the customer."""
        return self._password
    
    @property
    def notifications(self):
        """! Get the customer's notifications.
        @return (List[str]): List of notifications.
        """
        return self.__notifications
    
    def bookings(self):
        """! Get the customer's bookings.
        @return (List[Booking]): List of bookings.
        """
        return self.__bookings


    def add_booking(self, new_booking):
        """! Add a new booking for the customer.
        @param new_booking (Booking): The new booking to add.
        @return (bool): True if the booking was successfully added, False otherwise.
        """
        for booking in self.bookings():
            if new_booking.movie.title == booking.movie.title and new_booking.screening == booking.screening and booking.status == 'Pending':
                return False
        self.__bookings.append(new_booking)
        return True
    

    def add_notification(self, notification):
        """! Add a notification for the customer.
        @param notification (str): The notification message to add.
        """
        self.__notifications.append(notification)
        

    def find_booking(self, booking_id):
        """! Find a booking by its ID.
        @param booking_id (str): The ID of the booking to find.
        @return (Optional[Booking]): The found booking or None if not found.
        """
        for booking in self.bookings():
            if int(booking_id) == booking.booking_id:
                return booking
        else:
            return None


    def cancel_booking(self, booking_id):
        """! Cancel a booking by its ID.
        @param booking_id (str): The ID of the booking to cancel.
        """
        for booking in self.bookings():
            if int(booking_id) == booking.booking_id:
                booking.status = 'Canceled'
        

    def search_movie_title(self, title: str, movies):
        """! Search for movies by title for guest users.
        @param title (str): The title of the movie to search for.
        @param movies: List of movies to search in.
        @return: List of matching movies.
        """
        return Base.search_movie_title(title, movies)


    def search_movie_lang(self, selected_language: str, filtered_movies):
        """! Search for movies by language for guest users.
        @param selected_language (str): The selected language to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_lang(selected_language, filtered_movies)


    def search_movie_genre(self, selected_genre: str, filtered_movies):
        """! Search for movies by genre for guest users.
        @param selected_genre (str): The selected genre to filter by.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_genre(selected_genre, filtered_movies)


    def search_movie_date(self, date_from: date, date_to: date, filtered_movies):
        """! Search for movies by release date for guest users.
        @param date_from (date): The starting date for the search.
        @param date_to (date): The ending date for the search.
        @param filtered_movies: List of movies to filter.
        @return: List of matching movies.
        """
        return Base.search_movie_date(date_from,date_to, filtered_movies)


    @classmethod
    def read_customers_from_file(cls):
        """! Read customers from a JSON file.
        @return: A list of customers data read from the file.
        """
        customers_data = cls.read_from_file(CUSTOMER_FILENAME)
        return customers_data


    def to_dict(self):
        """Convert the Customer object to a dictionary.
        @returns:dict: A dictionary representation of the Customer object.
        """
        customer_dict = {
            "name": self.name,
            "address": self.address,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "password": self.password,  # Note: This should not be used in practice for security reasons.
        }
        return customer_dict


class Movie(Base):
    """! The Movie class: Represents a movie with details."""
    next_id = 100

    def __init__(self, title: str, language: str, genre: str, country: str, release_date: date, duration_in_mins: int, description: str, is_active = True) -> None:
        """! Constructor for the Movie class.
        @param title (str): The title of the movie.
        @param language (str): The language of the movie.
        @param genre (str): The genre of the movie.
        @param country (str): The country of the movie.
        @param release_date (date): The release date of the movie.
        @param duration_in_mins (int): The duration of the movie in minutes.
        @param description (str): A description of the movie.
        @param screenings (list): A list of screenings of the movie.
        """
        self.__id = Movie.next_id          # Unique movie ID
        self.__title = title               # The title of the movie
        self.__language = language         # The language of the movie
        self.__genre = genre               # The genre of the movie
        self.__country = country           # The country of the movie
        self.__release_date = release_date # The release date of the movie
        self.__duration_in_mins = duration_in_mins  # Duration of the movie in minutes
        self.__description = description   # A description of the movie
        self.__screenings = []             # List of screenings for this movie
        self.__is_active = True            # Movie status
        Movie.next_id += 1                 # Increment the movie ID counter

    @property
    def id(self):
        """! Get the ID of the movie.
        @return (int): The movie's unique ID.
        """
        return self.__id

    @property
    def title(self):
        """! Get the title of the movie.
        @return (str): The movie's title.
        """
        return self.__title

    @property
    def language(self):
        """! Get the language of the movie.
        @return (str): The language of the movie.
        """
        return self.__language

    @property
    def genre(self):
        """! Get the genre of the movie.
        @return (str): The genre of the movie.
        """
        return self.__genre

    @property
    def country(self):
        """! Get the country of the movie.
        @return (str): The country of the movie.
        """
        return self.__country

    @property
    def release_date(self):
        """! Get the release date of the movie.
        @return (date): The release date of the movie.
        """
        return self.__release_date

    @property
    def duration_in_mins(self):
        """! Get the duration of the movie in minutes.
        @return (int): The duration of the movie in minutes.
        """
        return self.__duration_in_mins

    @property
    def description(self):
        """! Get the description of the movie.
        @return (str): A description of the movie.
        """
        return self.__description
    
    @property
    def screenings(self):
        """! Get the list of screenings for the movie.
        @return (List[Screening]): A list of screenings for this movie.
        """
        return self.__screenings
    
    @property
    def is_active(self):
        return self.__is_active
    
    def deactivate(self):
        self.__is_active = False
    
    def add_screening(self, screening_object):
        """! Add a screening to the movie's list of screenings.
        @param screening_object (Screening): The screening to add.
        """
        self.__screenings.append(screening_object)
        self.__screenings.sort(key=lambda x: x.screening_date)

        
    def find_screening(self, screening_id):
        """! Find a screening by its ID.
        @param screening_id (str): The ID of the screening to find.
        @return (Optional[Screening]): The screening object if found, or None if not found.
        """
        for screening in self.screenings:
            print(f'debug{screening}')
            if screening.screening_id == int(screening_id):
                print(f"debug {screening.screening_id}")
                return screening
        return None
    
        
    def get_screening_date_list(self):
        """! Get a list of unique screening dates that are active and after the current date.
        @return (List[date]): A list of unique screening dates.
        """
        current_date = date.today()
        # Create a set of unique dates that are after the current date
        unique_dates = set()
        for screening in self.screenings:
            screening_date = datetime.strptime(screening.screening_date, "%Y-%m-%d").date()
            if screening_date >= current_date and screening.is_active == True:
                unique_dates.add(screening_date)
        # Convert to a list
        screening_date_list = sorted(list(unique_dates))
        return screening_date_list


    @classmethod
    def update_movie_status_to_inactive(cls, movie_id):
        """! Update the status of a movie to inactive in the JSON file.
        @param movie_id (int): The ID of the movie to be updated.
        """
        movies_data = cls.read_from_json(MOVIES_FILENAME)
        for movie_data in movies_data:
            if movie_data["movie_id"] == movie_id:
                movie_data["is_active"] = False
        cls.save_to_file(movies_data, MOVIES_FILENAME)


    @classmethod
    def update_movies_json(cls, movies):
        """! Update the JSON file with movie data.
        @param movies (List[Movie]): A list of movie objects to be saved to the JSON file.
        """
        movies_data = [movie.to_dict() for movie in movies]
        cls.save_to_file(movies_data, MOVIES_FILENAME)


    @classmethod
    def save_new_movie_to_file(cls, movie):
        """! Save a new movie to a JSON file.
        @param movie (Movie): The movie object to be added to the JSON file.
        """
        # Load existing movie data from movies.json if it exists
        movies_data = cls.read_from_file(MOVIES_FILENAME)
        # Append the new movie data to the existing data
        movies_data.append(movie.to_dict())
        # Save the updated movie data back to movies.json
        cls.save_to_file(movies_data, MOVIES_FILENAME)


    def to_dict(self):
        """Convert Movie object to a dictionary."""
        return {
            "movie_id": self.id,
            "title": self.title,
            "language": self.language,
            "genre": self.genre,
            "country": self.country,
            "release_date": self.release_date,
            "duration": self.duration_in_mins,
            "description": self.description,
            "is_active": self.is_active,
            "screenings": self.screenings,
        }


    def __str__(self):
        """! Get a string representation of the movie object.
        @return (str): A string representation of the movie.
        """
        return f"Movie ID: {self.__id}\nTitle: {self.__title}\nLanguage: {self.__language}\nGenre: {self.__genre}\nCountry: {self.__country}\nRelease Date: {self.__release_date}\nDuration (mins): {self.__duration_in_mins}\nDescription: {self.__description}"


class CinemaHallSeat:
    """! The CinemaHallSeat class: Represents a seat in a cinema hall with details such as seat number, row number, reservation status, and price."""
    def __init__(self, seat_number, row_number, is_reserved, seat_price):
        """! Constructor for CinemaHallSeat class.
        @param seat_number (int): The seat number.
        @param row_number (int): The row number.
        @param is_reserved (bool): Indicates whether the seat is reserved.
        @param seat_price (float): The price of the seat.
        """
        self.__seat_id = str(row_number) + str(seat_number)
        self.__seat_number = seat_number
        self.__row_number = row_number
        self.__is_reserved = is_reserved
        self.__seat_price = seat_price

    @property
    def seat_id(self):
        """! Get the unique identifier of the seat.
        @return (str): The seat's unique ID.
        """
        return self.__seat_id

    @property
    def seat_number(self):
        """! Get the seat number.
        @return (int): The seat number.
        """
        return self.__seat_number
    
    @property
    def row_number(self):
        """! Get the row number.
        @return (int): The row number.
        """
        return self.__row_number
    
    @property
    def is_reserved(self):
        """! Get the reservation status of the seat.
        @return (bool): True if the seat is reserved, False if it's available.
        """
        return self.__is_reserved

    @is_reserved.setter
    def is_reserved(self, value):
        """! Set the reservation status of the seat.
        @param value (bool): True to mark the seat as reserved, False to mark it as available.
        """
        self.__is_reserved = value

    @property
    def seat_price(self):
        """! Get the price of the seat.
        @return (float): The seat's price.
        """
        return self.__seat_price
    
    @seat_price.setter
    def seat_price(self, price):
        """! Set the price of the seat.
        @param price (float): The new price for the seat.
        """
        self.__seat_price = price
    

    def to_json(self):
        """! Convert the seat information to a dictionary.
        @return (Dict): A dictionary representation of the seat.
        """
        return {
            "seat_number": self.__seat_number,
            "row_number": self.__row_number,
            "is_reserved": self.__is_reserved,
            "seat_price": self.__seat_price,
        }


    @classmethod
    def initialise_seats(self, hall, price): 
        """! Initialize seats for the screening.
        @param hall (CinemaHall): The cinema hall for which seats are being initialized.
        @param price (float): The price of the seats.
        @return (List[CinemaHallSeat]): A list of initialized CinemaHallSeat objects.
        """ 
        seats = []    
        for row_number in range(1, hall.capacity // 10 + 1):  # Assuming 10 seats per row
            for seat_number in range(1, 11):  # 10 seats per row
                seat = CinemaHallSeat(seat_number, row_number, False, price)  # Initialize seats
                seats.append(seat)
        return seats


    def __str__(self):
        """! Get a string representation of the seat.
        @return (str): A string representing the seat's status.
        """
        return f"Seat {self.seat_id} - {'Reserved' if self.is_reserved else 'Available'} - Price {self.seat_price}"


class CinemaHall(Base):
    """! The CinemaHall class: Represents a movie hall with a name and seating capacity."""
    def __init__(self, hall_name: str, capacity: int) -> None:
        """! Constructor for the Hall class.
        @param hall_name (str): The name of the hall.
        @param capacity (int): The seating capacity of the hall.
        """
        self.__hall_name = hall_name  # Name of the hall
        self.__capacity = capacity    # Seating capacity of the hall

    @property
    def hall_name(self):
        """! Get the name of the cinema hall.
        @return (str): The name of the hall.
        """
        return self.__hall_name
    
    @property
    def capacity(self):
        """! Get the seating capacity of the cinema hall.
        @return (int): The seating capacity.
        """
        return self.__capacity

    @property
    def seats(self):
        """! Get the list of seats in the cinema hall.
        @return (list): List of cinema hall seats.
        """
        return self.__seats


    @classmethod
    def read_hall_from_file(cls):
        """! Create CinemaHall objects by reading data from a file.
        This method reads hall data from a file, creates CinemaHall objects, and appends them to a list.
        @return (list): List of CinemaHall objects created from the file data.
        """
        halls_data = cls.read_from_file(HALL_FILENAME)
        return halls_data


class Screening(Base):
    """! The Screening class: Represents a movie screening with details."""
    next_id = 100
    def __init__(self, movie_id, screening_date, start_time, end_time, hall: CinemaHall, seats, is_active=True) -> None:
        """! Constructor for the Screening class.
        @param movie_id (int): The ID of the associated movie.
        @param screening_date (str): The date of the screening.
        @param start_time (str): The start time of the screening.
        @param end_time (str): The end time of the screening.
        @param hall (CinemaHall): The cinema hall where the screening takes place.
        @param seats (list): The list of CinemaHallSeat objects for the screening.
        @param is_active (bool): The status of the screening (active or inactive).
        """
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
        """! Get the screening ID.
        @return (int): The unique ID of the screening.
        """
        return self.__screening_id
    
    @property
    def movie_id(self):
        """! Get the associated movie ID.
        @return (int): The ID of the movie associated with the screening.
        """
        return self.__movie_id

    @property
    def screening_date(self):
        """! Get the date of the screening.
        @return (str): The date when the screening takes place.
        """
        return self.__screening_date
    
    @property
    def start_time(self):
        """! Get the start time of the screening.
        @return (str): The time when the screening begins.
        """
        return self.__start_time
    
    @property
    def end_time(self):
        """! Get the end time of the screening.
        @return (str): The time when the screening ends.
        """
        return self.__end_time
    
    @property
    def hall(self):
        """! Get the cinema hall of the screening.
        @return (CinemaHall): The cinema hall where the screening is held.
        """
        return self.__hall
    
    @property
    def seats(self):
        """! Get the list of seats available in the screening.
        @return (list): A list of CinemaHallSeat objects representing the seats in the screening.
        """
        return self.__seats
    
    @property
    def is_active(self):
        """! Check the status of the screening (active or inactive).
        @return (bool): True if the screening is active, False if it's inactive.
        """
        return self.__is_active
    
    @is_active.setter
    def is_active(self, status):
        """! Set the status of the screening to inactive.
        @param status (bool): The status to set (True for active, False for inactive).
        """
        self.__is_active = False
    
    def to_dict(self):
        """! Convert the screening details to a dictionary.
        @return (dict): A dictionary containing screening details.
        """
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


    def find_seat_by_identifier(self, row_number, seat_number):
        """! Find a seat in the screening by its row and seat number.
        @param row_number (int): The row number of the seat.
        @param seat_number (int): The seat number.
        @return (CinemaHallSeat|None): The CinemaHallSeat object if found, None if not found.
        """
        for seat in self.seats:
            if seat.row_number == row_number and seat.seat_number == seat_number:
                return seat  
        return None 
    
    def find_seat_by_id(self, seat_id):
        """! Find a seat in the screening by its unique identifier.
        @param seat_id (str): The unique identifier of the seat.
        @return (CinemaHallSeat|None): The CinemaHallSeat object if found, None if not found.
        """
        for seat in self.seats:
            if seat.seat_id == str(seat_id):
                return seat  
        return None  
    

    @classmethod
    def save_new_screening_to_json(cls, new_screening):
        """! Save a new screening to a JSON file.
        @param new_screening (Screening): The new screening object to be saved.
        """
        existing_data = cls.read_from_file(SCREENINGS_FILENAME)
        existing_data.append(new_screening.to_dict())
        cls.save_to_file(existing_data, SCREENINGS_FILENAME)


    @classmethod
    def update_screening_status_to_inactive_to_json(cls, screening_id):
        """! Update the status of a screening to inactive in the JSON file.
        @param screening_id (int): The ID of the screening to be updated.
        """
        screenings_data = cls.read_from_file(SCREENINGS_FILENAME)

        for screening_data in screenings_data:
            if screening_data["screening_id"] == screening_id:
                screening_data["is_active"] = False

        cls.save_to_file(screenings_data, SCREENINGS_FILENAME)


    @classmethod
    def update_reserved_seats_to_json(cls, screening_id, reserved_seats_id, is_reserved):
        """! Update the reservation status of seats for a screening in the JSON file.
        @param screening_id (int): The ID of the screening.
        @param reserved_seats_id (list): List of seat IDs to be updated.
        @param is_reserved (bool): The reservation status to be set for the seats.
        """
        screening_data_list = cls.read_from_file(SCREENINGS_FILENAME)

        for screening_data in screening_data_list:
            if screening_data["screening_id"] == screening_id:
                for reserved_seat_id in reserved_seats_id:
                    for seat_data in screening_data["seats"]:
                        if reserved_seat_id == str(seat_data["row_number"]) + str(seat_data["seat_number"]):
                            seat_data["is_reserved"] = is_reserved

        cls.save_to_file(screening_data_list, SCREENINGS_FILENAME)


    def __str__(self):
        """! Get a string representation of the screening.
        @return (str): A string describing the screening, including its ID, start time, end time, and hall.
        """
        return f"Screening id: {self.screening_id}\n" \
               f"Start Time: {self.start_time}\n" \
               f"End Time: {self.end_time}\n" \
               f"Hall: {self.hall}\n" \


class Coupon(Base):
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
        @return(bool): True if the coupon is valid, otherwise False.
        """
        current_date = date.today()
        if self.__expiration_date >= current_date:
            return True
        else:
            return False
        

    @classmethod
    def read_coupons_from_json(cls):  
        """! Read coupon data from a JSON file and create Coupon objects.
        @return (list): A list of Coupon objects.
        """  
        coupons = []    
        coupons_data = cls.read_from_file(COUPON_FILENAME)
        for item in coupons_data:
            coupon_code = item.get('coupon_code', '')
            discount = item.get('discount_percentage', 0.0)
            expiry_date_str = item.get('expiration_date', '')
            # Parse the date string into a datetime object
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
            
            # Create a Coupon object and add it to the list
            coupon = Coupon(coupon_code, discount, expiry_date)
            coupons.append(coupon)
        return coupons


class Payment(ABC):
    """! The Payment class: Represents a payment with common attributes."""
    def __init__(self, payment_id: int, amount: float, created_on: datetime, coupon: Optional[Coupon]):
        """! Constructor for the Payment class.
        @param payment_id (int): The unique payment ID.
        @param amount (float): The payment amount.
        @param created_on (datetime): The date and time when the payment was created.
        @param coupon (Coupon): An optional coupon associated with the payment.
        """
        self._payment_id = payment_id
        self._amount = amount
        self._created_on = created_on
        self._coupon = coupon

    @abstractmethod
    def process_payment(self):
        """! Process the payment (abstract method to be implemented by subclasses)."""
        pass


    @classmethod
    def read_payments_from_file(cls):
        """! Read payment data from a file and return a list of payment records.
        @return (list): A list of payment data.
        """
        try:
            with open(PAYMENTS_FILENAME, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {PAYMENTS_FILENAME}")
            return []


class CreditCard(Payment, Base):
    """! The CreditCard class: Represents a credit card payment with additional attributes."""
    def __init__(self, payment_id:int, amount: float, created_on: datetime, coupon: Optional[Coupon],
                 credit_card_number: str, card_type: str, expiry_date: datetime, name_on_card: str):
        """! Constructor for the CreditCard class.
        @param payment_id (int): The unique payment ID.
        @param amount (float): The payment amount.
        @param created_on (datetime): The date and time when the payment was created.
        @param coupon (Coupon): An optional coupon associated with the payment.
        @param credit_card_number (str): The credit card number.
        @param card_type (str): The type of credit card (e.g., Visa, MasterCard).
        @param expiry_date (datetime): The credit card's expiry date.
        @param name_on_card (str): The name on the credit card.
        """
        super().__init__(payment_id, amount, created_on, coupon)
        self.__credit_card_number = credit_card_number
        self.__card_type = card_type
        self.__expiry_date = expiry_date
        self.__name_on_card = name_on_card
    
    @property
    def payment_id(self):
        """! Get the unique payment ID.
        @return (int): The unique payment ID.
        """
        return self._payment_id

    @property
    def credit_card_number(self):
        """! Get the credit card number.
        @return (str): The credit card number.
        """
        return self.__credit_card_number
    
    @property
    def amount(self):
        """! Get the payment amount.
        @return (float): The payment amount.
        """
        return self._amount
    
    @property
    def coupon(self):
        """! Get the associated coupon for the payment (if available).
        @return (Coupon): The associated coupon object, or None if no coupon is associated.
        """
        return self._coupon

    def to_dict(self):
        """! Convert the CreditCard payment to a dictionary.
        @return (dict): A dictionary representation of the payment details.
        """
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
        """! Process the credit card payment (placeholder implementation).
        In a real application, this method would interact with a payment gateway or service.
        """
        print(f"Processing a payment using credit card ending in {self.credit_card_number[-4:]}")
        return True
    
    def process_refund(self):
        """! Process a refund for the credit card payment (placeholder implementation).
        In a real application, this method would interact with a payment gateway or service.
        """    
        print(f"Processing a refund payment using credit card ending in {self.credit_card_number[-4:]}")
        return True


    @classmethod
    def save_payment_to_json(cls, payment):
        """! Save the payment details to a JSON file.
        @param payment: The CreditCard payment to save.
        """
        if payment is None:
            return
        existing_data = cls.read_from_file(PAYMENTS_FILENAME)
        existing_data.append(payment.to_dict())
        cls.save_to_file(existing_data, PAYMENTS_FILENAME)


class DebitCard(Payment):
    """! The DebitCard class: Represents a payment made using a debit card."""
    def __init__(self, payment_id: int, amount: float, created_on: datetime, coupon: Optional[Coupon],
                 card_number: str, bank_name: str, name_on_card: str):
        """! Constructor for the DebitCard class.
        @param payment_id (int): The unique payment ID.
        @param amount (float): The payment amount.
        @param created_on (datetime): The date and time when the payment was created.
        @param coupon (Optional[Coupon]): An optional coupon applied to the payment.
        @param card_number (str): The debit card number.
        @param bank_name (str): The name of the bank associated with the debit card.
        @param name_on_card (str): The name of the cardholder.
        """
        super().__init__(payment_id, amount, created_on, coupon)
        self.__card_number = card_number
        self.__bank_name = bank_name
        self.__name_on_card = name_on_card

    def process_payment(self):
        """! Process a payment using a debit card.
        This method should contain the logic to process a payment using a debit card, such as communicating with a payment gateway.
        """
        pass


class Booking(Base):
    """! The Notification class: Represents a notification sent to a user. """
    next_id = 1
    def __init__(self, customer: Customer, movie: Movie, screening: Screening, num_of_seats: int, selected_seats: List[CinemaHallSeat], created_on: date, total_amount: float, status: str, payment = None, coupon = None) -> None:
        """! Constructor for the Booking class.
        @param customer (Customer): The customer who made the booking.
        @param movie (Movie): The movie being booked.
        @param screening (Screening): The screening for which the booking is made.
        @param num_of_seats (int): The number of seats booked.
        @param selected_seats (List[CinemaHallSeat]): List of selected cinema hall seats.
        @param created_on (date): The date on which the booking was created.
        @param total_amount (float): The total payment amount.
        @param status (str): The status of the booking (e.g., 'active', 'canceled').
        @param payment (Optional[Payment]): The payment associated with the booking.
        @param coupon (Optional[Coupon]): An optional coupon applied to the booking.
        """
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
        """! Get the booking ID.
        @return (int): The ID of the booking.
        """
        return self.__booking_id
    
    @property
    def customer(self):
        """! Get the customer for the booking.
        @return (str): The customer associated with the booking.
        """
        return self.__customer

    @property
    def movie(self):
        """! Get the movie for the booking.
        @return (str): The movie associated with the booking.
        """
        return self.__movie
    
    @property
    def screening(self):
        """! Get the screening for the booking.
        @return (str): The screening associated with the booking.
        """
        return self.__screening
    
    @property
    def num_of_seats(self):
        """! Get the number of seats for the booking.
        @return (int): The number of seats booked.
        """
        return self.__num_of_seats

    @property
    def selected_seats(self):
        """! Get the selected seats for the booking.
        @return (list): A list of selected seats.
        """
        return self.__selected_seats
    
    @property
    def created_on(self):
        """! Get the creation date of the booking.
        @return (str): The date when the booking was created.
        """
        return self.__created_on
    
    @property
    def total_amount(self):
        """! Get the total amount for the booking.
        @return (float): The total cost of the booking.
        """
        return self.__total_amount
    
    @property
    def status(self):
        """! Get the status of the booking.
        @return (str): The current status of the booking.
        """
        return self.__status
    
    @status.setter
    def status(self, status):
        """! Set the status of the booking.
        @param status (str): The new status to set for the booking.
        """
        self.__status = status
    
    @property
    def coupon(self):
        """! Get the coupon applied to the booking.
        @return (str): The coupon code applied to the booking.
        """
        return self.__coupon
    
    @coupon.setter
    def coupon(self, coupon):
        """! Set the coupon for the booking.
        @param coupon (str): The coupon code to apply to the booking.
        """
        self.__coupon = coupon

    @total_amount.setter
    def total_amount(self, total_amount):
        """! Set the total amount for the booking.
        @param total_amount (float): The new total amount to set for the booking.
        """
        self.__total_amount = total_amount

    @property
    def payment(self):
        """! Get the payment information for the booking.
        @return (Payment): The payment details associated with the booking.
        """
        return self.__payment

    @payment.setter
    def payment(self, apayment):
        """! Set the payment information for the booking.
        @param apayment (Payment): The payment details to associate with the booking.
        """
        self.__payment = apayment


    def to_dict(self):
        """! Convert the booking to a dictionary for JSON serialization.
        @return (Dict[str, Any]): A dictionary representation of the booking.
        """
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
    def update_payment_and_status(cls, booking_id, payment_id, new_status):
        """! Update payment and status of a booking.
        @param booking_id (int): The ID of the booking to update.
        @param payment_id (int): The ID of the associated payment.
        @param new_status (str): The new status of the booking.
        """
        bookings_info = cls.read_from_file(BOOKINGS_FILENAME)
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                booking_info["payment_id"] = payment_id
                booking_info["status"] = new_status

        cls.save_to_file(bookings_info, BOOKINGS_FILENAME)


    @classmethod
    def update_status_to_canceled(cls, booking_id, new_status):
        """! Update the status of a booking to 'canceled'.
        @param booking_id (int): The ID of the booking to update.
        @param new_status (str): The new status to set for the booking.
        """
        bookings_info = cls.read_from_file(BOOKINGS_FILENAME)
        for booking_info in bookings_info:
            if booking_info["booking_id"] == int(booking_id):
                booking_info["status"] = new_status

        cls.save_to_file(bookings_info, BOOKINGS_FILENAME)


    @classmethod
    def save_new_bookings_to_json(cls, booking):
        """! Save a new booking to a JSON file.
        @param booking: The booking object to be saved.
        @type booking: Booking
        """
        if os.path.exists(BOOKINGS_FILENAME) and os.path.getsize(BOOKINGS_FILENAME) > 0:
            existing_data = cls.read_from_file(BOOKINGS_FILENAME)

            # Append the new booking data to the existing data
            existing_data.append(booking.to_dict())

        cls.save_to_file(existing_data, BOOKINGS_FILENAME)


    def __str__(self):
        """! Get a formatted string representation of the Booking object.
        @return: A string containing formatted booking information.
        """
        return f"Booking ID: {self.__booking_id}\n" \
               f"Customer: {self.__customer}\n" \
               f"Screening: {self.__screening}\n" \
               f"Number of Seats: {self.__num_of_seats}\n" \
               f"Selected Seats: {', '.join(map(str, self.__selected_seats))}\n" \
               f"Created On: {self.__created_on}\n" \
               f"Total Amount: {self.__total_amount}\n" \
               f"Payment: {self.__payment}\n" \
               f"Status: {self.__status}"
    

class Notification(Base):
    """! The Notification class: Represents a notification sent to a user. """
    next_id = 100
    def __init__(self, customer, subject: str, message: str, date_time: datetime,  booking: Booking = None) -> None:
        """
        Initialize a new Notification.
        @param customer: The customer to whom the notification is sent.
        @type customer: Customer
        @param subject: The subject of the notification.
        @type subject: str
        @param message: The message content of the notification.
        @type message: str
        @param date_time: The date and time when the notification is created.
        @type date_time: datetime
        @param booking: The booking associated with the notification (optional).
        @type booking: Booking, optional
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
        """! Get the unique notification ID.
        @return (int): The unique notification ID.
        """
        return self.__notification_id
    
    @property
    def customer(self):
        """! Get the customer to whom the notification is sent.
        @return (Customer): The customer associated with the notification.
        """
        return self.__customer
    
    @property
    def subject(self):
        """! Get the subject of the notification.
        @return (str): The subject of the notification.
        """
        return self.__subject
    
    @property
    def message(self):
        """! Get the message content of the notification.
        @return (str): The message content of the notification.
        """
        return self.__message
    
    @property
    def date_time(self):
        """! Get the date and time when the notification is created.
        @return (datetime): The date and time when the notification is created.
        """
        return self.__date_time
    
    @property
    def booking(self):
        """! Get the booking associated with the notification (if any).
        @return (Booking): The booking associated with the notification, or None.
        """
        return self.__booking

    @classmethod
    def save_notification_to_json(cls, notification):
        """! Save a notification to a JSON file.
        @param notification: The notification object to be saved.
        @type notification: Notification
        """
        if notification is None:
            return

        existing_data = cls.read_from_file(NOTIFICATION_FILENAME)

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
        cls.save_to_file(existing_data, NOTIFICATION_FILENAME)