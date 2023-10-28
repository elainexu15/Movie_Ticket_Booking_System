from .models import *
import json


class CinemaController:
    def __init__(self):
        self.__customers = []
        self.__admins = []
        self.__front_desk_staffs = []
        self.__movies = []
        self.__halls = []
        self.__coupons = []

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

    def find_customer(self, username):
        for customer in self.__customers:
            if customer.username == username:
                return customer
        return None

    def find_movie(self, id):
        for movie in self.__movies:
            if movie.id == id:
                print(type(movie.id))
                print(type(id))
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


    # Method to read movie data from a JSON file and create Movie objects
    def add_movies_from_json(self, file_name):
        try:
            with open(file_name, 'r') as json_file:
                movie_data = json.load(json_file)
                
                if "movies" in movie_data:
                    for movie_info in movie_data["movies"]:
                        title = movie_info.get("title", "")
                        language = movie_info.get("language", "")
                        genre = movie_info.get("genre", "")
                        country = movie_info.get("country", "")
                        release_date = movie_info.get("release_date", "")
                        duration_in_minutes = movie_info.get("duration", 0)  # Replace 0 with a default value
                        description = movie_info.get("description", "")
                        movie_object = Movie(title, language, genre, country, release_date, duration_in_minutes, description)
                        self.add_movie(movie_object)
                else:
                    print(f"Error: The 'movies' key is missing in the JSON file '{file_name}'.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")


    # Method to read hall data from a file and create Cinema Hall objects
    def add_hall_from_file(self, file_name):
        try:
            with open(file_name, 'r',  encoding='utf-8') as file:
                for line in file:
                    data = line.strip().split(',')
                    hall_name, capacity = data[0], int(data[1])
                    cinema_hall_object = CinemaHall(hall_name, capacity)
                    self.add_hall(cinema_hall_object)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_name}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_name}': {str(e)}")

    # Initialize seats for the screening
    def initialise_seats(self, hall, price):  
        seats = []    
        print(price)  
        for row_number in range(1, hall.capacity // 10 + 1):  # Assuming 10 seats per row
            for seat_number in range(1, 11):  # 10 seats per row
                seat = CinemaHallSeat(seat_number, row_number, False, price)  # Initialize seats
                seats.append(seat)
        return seats


    # ======= read screenings data =======
    def add_screening_from_file(self, movie_id):
        # Read the JSON file for the given movie_id
        filename = f'app/database/screenings/screenings_{movie_id}.json'
        # find movie objec
        movie = self.find_movie(movie_id)
        try:
            with open(filename, 'r') as json_file:
                screening_data_list = json.load(json_file)
            
            for screening_data in screening_data_list:
                # Extract screening data
                screening_date = screening_data.get("screening_date")
                start_time = screening_data.get("start_time")
                end_time = screening_data.get("end_time")
                hall_name = screening_data.get("hall_name")
                price = screening_data.get("price")
                seats_data = screening_data.get("seats", [])
                
                # Find the hall based on the hall_name
                hall = self.find_hall(hall_name)
                
                # Create a list to store seat objects
                seats = []
                
                # Loop through the seats data and create seat objects
                for seat_data in seats_data:
                    seat_number = seat_data.get("seat_number")
                    row_number = seat_data.get("row_number")
                    is_reserved = seat_data.get("is_reserved")
                    seat_price = seat_data.get("seat_price")
                    
                    seat = CinemaHallSeat(seat_number, row_number, is_reserved, seat_price)
                    seats.append(seat)
                
                # Create a CinemaScreening object
                screening = Screening(screening_date, start_time, end_time, hall, seats)
                
                # Add the screening to the movie
                movie.add_screening(screening)
        
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")


    def read_coupons_from_json(self, json_file):        
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                for item in data:
                    coupon_code = item.get('coupon_code', '')
                    discount = item.get('discount_percentage', 0.0)
                    expiry_date_str = item.get('expiration_date', '')
                    print(coupon_code)
                    # Parse the date string into a datetime object
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
                    
                    # Create a Coupon object and add it to the list
                    coupon = Coupon(coupon_code, discount, expiry_date)
                    self.__coupons.append(coupon)
        
        except FileNotFoundError:
            print(f"File '{json_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{json_file}'.")
        

    def read_bookings_from_json_file(self, json_filename):
        bookings = []
        
        try:
            with open(json_filename, 'r') as json_file:
                booking_info = json.load(json_file)
                print(booking_info)
                selected_seats_id_list = booking_info["selected_seats"]
               # Convert the movie_id from string to integer
                movie_id = int(booking_info["movie_id"])
                movie = self.find_movie(movie_id)
                if movie is not None:
                    print(f"Movie with ID {movie_id} found.")
                else:
                    print(f"Movie with ID {movie_id} not found.")
                screening_id = int(booking_info["screening_id"])

                screening=movie.find_screening(booking_info["screening_id"])
                if screening is not None:
                    print(f"screening with ID {screening_id} not found.")
        


                customer=self.find_customer(booking_info["customer_username"])
                num_of_seats=booking_info["num_of_seats"]
                
                selected_seats=[]
                for seat_id in selected_seats_id_list:
                    seat = screening.find_seat_by_id(seat_id) 
                    selected_seats.append(seat)
                    print(seat)
                
                created_on=date.fromisoformat(booking_info["created_on"])
                total_amount=float(booking_info["total_amount"])
                status=booking_info["status"]

                for booking_info in booking_info:
                    booking = Booking(
                        customer=customer,
                        movie=movie,
                        screening=screening,
                        num_of_seats=num_of_seats,
                        selected_seats=selected_seats,
                        created_on=created_on,
                        total_amount=total_amount,
                        status=status)
                    bookings.append(booking)
                    
        except FileNotFoundError:
            print(f"File not found: {json_filename}")
        except Exception as e:
            print(f"An error occurred while reading the JSON file: {str(e)}")
        
        return bookings


    def add_booking_to_customer(self, customer):
        filename = f'app/database/bookings/{customer.username}_bookings.json'
        print(f'app/database/bookings/{customer.username}_bookings.json')
        bookings = self.read_bookings_from_json_file(filename)
        print(bookings)
        for booking in bookings:
            customer.add_booking(booking)

    def load_database(self):
        self.add_customers_from_file('app/database/customers.txt')
        self.add_admins_from_file('app/database/admins.txt')
        self.add_front_desk_staffs_from_file('app/database/front_desk_staffs.txt')
        self.add_movies_from_json('app/database/movies.json')
        self.add_hall_from_file('app/database/cinema_hall.txt')
        for movie in self.all_movies:
            self.add_screening_from_file(movie.id)
        self.read_coupons_from_json('app/database/coupons.json')
        for customer in self.all_customers:
            self.add_booking_to_customer(customer)

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


# ====== filter screenings ========
    def find_screening_by_date_and_time(self, movie, screening_date, start_time):
        # Convert the input values to datetime objects
        print(type(screening_date))
        print(type(start_time))
        # Iterate through the movie's screenings to find a matching screening
        for screening in movie.screenings:
            if (
                screening.screening_date == screening_date and
                screening.start_time == start_time
            ):
                return screening

        # If no matching screening is found, return None
        return None
    

# ====== save booking =======
    def save_bookings_to_json(self, customer, booking):
        if customer is None:
            return
        try:
            # Use the customer's username as the filename
            filename = f"app/database/bookings/{customer.username}_bookings.json"
            
            bookings_data = booking.to_dict()  
            with open(filename, 'w') as json_file:
                json.dump(bookings_data, json_file, default=str, indent=4)

            print(f"Bookings for {customer.username} have been saved to {filename}")
        except Exception as e:
            print(f"An error occurred while saving bookings: {str(e)}")


