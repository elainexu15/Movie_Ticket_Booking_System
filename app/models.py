from abc import ABC, abstractmethod
from datetime import date, datetime

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


    def search_movie_date(self, selected_year: date, filtered_movies):
        # Implement search by movie release date for guests
        matching_movies = []   
        current_year = datetime.now().year
        if selected_year == 'other': 
            for movie in filtered_movies:  # Assuming you have a list of movies in the General class
                if movie.year is not None and movie.year < current_year-12:
                    matching_movies.append(movie)
        else:
            for movie in filtered_movies:  # Assuming you have a list of movies in the General class
                if movie.year is not None and int(selected_year) == movie.year:
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
    def year(self):
        # Convert the release date to a datetime object
        release_date = datetime.fromisoformat(self.release_date)
        # Extract the year from the release date
        release_year = release_date.year
        return release_year

    @property
    def duration_in_mins(self):
        return self.__duration_in_mins

    @property
    def description(self):
        return self.__description