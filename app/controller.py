from .models import *


class CinemaController:
    def __init__(self):
        self.__customers = []
        self.__admins = []
        self.__front_desk_staffs = []
        self.__movies = []

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
            


    def find_customer(self, username):
        for customer in self.__customers:
            if customer.username == username:
                return customer
        return None


    def add_customer(self, customer):
        self.__customers.append(customer)
    
    def add_admin(self, admin):
        self.__admins.append(admin)

    def add_front_desk_staff(self, front_desk_staff):
        self.__front_desk_staffs.append(front_desk_staff)

    def add_movie(self, movie_object):
        self.__movies.append(movie_object)
            

    def register_customer(self, name, address, email, phone, username, hashed_password) -> bool:
        # Check if the username already exists
        if self.find_customer(username):
            return False
        new_customer = Customer(name, address, email, phone, username, hashed_password)
        self.add_customer(new_customer)
        with open('app/database/customers.txt', 'a') as file:
            file.write(f"{new_customer.name},{new_customer.address},{new_customer.email},{new_customer.phone},{new_customer.username},{new_customer.password}\n")
        return True


    def add_admins_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
                    admin_object = Admin(name, address, email, phone, username, password)
                    self.add_admin(admin_object)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")


    def add_front_desk_staffs_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
                    front_desk_staff_object = FrontDeskStaff(name, address, email, phone, username, password)
                    self.add_front_desk_staff(front_desk_staff_object)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")



    # Method to read customer data from a file and create Customer objects
    def add_customers_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    name, address, email, phone, username, password = data[0], data[1], data[2], data[3], data[4], data[5]
                    customer_object = Customer(name, address, email, phone, username, password)
                    self.add_customer(customer_object)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")

   # Method to read movie data from a file and create Movie objects
    def add_movies_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    title, language, genre, country, release_date, duration_in_minutes, description = data[0], data[1], data[2], data[3], data[4], data[5], data[6]
                    movie_object = Movie(title, language, genre, country, release_date, duration_in_minutes, description)
                    self.add_movie(movie_object)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")
    
    def load_database(self):
        self.add_customers_from_file('app/database/customers.txt')
        self.add_admins_from_file('app/database/admins.txt')
        self.add_front_desk_staffs_from_file('app/database/front_desk_staffs.txt')
        self.add_movies_from_file('app/database/movies.txt')




    # ======== get movie details ========
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
    

    # ======== get movie details ========
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

