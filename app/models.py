from abc import ABC, abstractmethod
from datetime import date

class General(ABC):
    pass

class Guest(General):
    pass

class Person(General, ABC):
    def __init__(self, name: str, address: str, email: str, phone: str) -> None:
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone

class User(Person, ABC):
    def __init__(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> None:
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password

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
        self.__movie_id = Movie.next_id    # Unique movie ID
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