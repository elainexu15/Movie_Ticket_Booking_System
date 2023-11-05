import json
import os
from datetime import date
from app.models import *
import pytest


# Define fixtures 
@pytest.fixture
def sample_movies():
    movie1 = Movie("TEST MOVIE 1", "English", "Action", "USA", date(2023, 1, 1), 120, "Description 1")
    movie2 = Movie("TEST MOVIE 2", "Spanish", "Comedy", "Spain", date(2023, 2, 15), 100, "Description 2")
    movie3 = Movie("TEST MOVIE 3", "French", "Drama", "France", date(2023, 3, 30), 130, "Description 3")
    movie4 = Movie("TEST MOVIE 4", "German", "Horror", "Germany", date(2023, 4, 10), 110, "Description 4")
    movie5 = Movie("TEST MOVIE 5", "Italian", "Romance", "Italy", date(2023, 5, 25), 105, "Description 5")
    sample_movies = [movie1, movie2, movie3, movie4, movie5]
    return sample_movies


# ========== Test Base class =========
def test_base_class_read_from_file(tmpdir):
    filename = os.path.join(tmpdir, 'test.json')
    data = [{"id": 1, "name": "Movie 1"}, {"id": 2, "name": "Movie 2"}]
    with open(filename, 'w') as file:
        json.dump(data, file)

    result = Base.read_from_file(filename)
    assert result == data

def test_base_class_save_to_file(tmpdir):
    filename = os.path.join(tmpdir, 'test.json')
    data = [{"id": 1, "name": "Movie 1"}, {"id": 2, "name": "Movie 2"}]
    Base.save_to_file(data, filename)

    with open(filename, 'r') as file:
        saved_data = json.load(file)

    assert saved_data == data


def test_base_class_search_movie_title(sample_movies):
    # Test searching movies by title
    result = Base.search_movie_title("Test", sample_movies)
    assert len(result) == 5

    result = Base.search_movie_title("1", sample_movies)
    assert len(result) == 1
    assert result[0].title == "TEST MOVIE 1"

def test_base_class_search_movie_lang(sample_movies):
    # Test searching movies by language
    result = Base.search_movie_lang("english", sample_movies)
    assert len(result) == 1

    result = Base.search_movie_lang("Chinese", sample_movies)
    assert len(result) == 0

def test_base_class_search_movie_genre(sample_movies):
    # Test searching movies by genre
    result = Base.search_movie_genre("Drama", sample_movies)
    assert len(result) == 1
    assert result[0].title == "TEST MOVIE 3"

    result = Base.search_movie_genre("Crime", sample_movies)
    assert len(result) == 0

def test_base_class_search_movie_date(sample_movies):
    # Test searching movies by release date
    date_from = date(2023, 2, 1)
    date_to = date(2023, 3, 1)
    result = Base.search_movie_date(date_from, date_to, sample_movies)
    assert len(result) == 1


# =========== Test Guest class ============
# create a Guest object
guest = Guest()

def test_guest_class_search_movie_title(sample_movies):
    # Test searching movies by title for guest users
    result = guest.search_movie_title("TEST", sample_movies)
    assert len(result) == 5

    result = guest.search_movie_title("1", sample_movies)
    assert len(result) == 1
    assert result[0].title == "TEST MOVIE 1"

def test_guest_class_search_movie_lang(sample_movies):
    # Test searching movies by language for guest users
    result = guest.search_movie_lang("english", sample_movies)
    assert len(result) == 1

    result = guest.search_movie_lang("Chinese", sample_movies)
    assert len(result) == 0

def test_guest_class_search_movie_genre(sample_movies):
    # Test searching movies by genre for guest users
    result = guest.search_movie_genre("Drama", sample_movies)
    assert len(result) == 1
    assert result[0].title == "TEST MOVIE 3"

    result = guest.search_movie_genre("Crime", sample_movies)
    assert len(result) == 0

def test_guest_class_search_movie_date(sample_movies):
    # Test searching movies by release date for guest users
    date_from = date(2023, 2, 1)
    date_to = date(2023, 3, 1)
    result = guest.search_movie_date(date_from, date_to, sample_movies)
    assert len(result) == 1


# =========== Test Admin class ===========
# Define a fixture to create an Admin instance for testing
@pytest.fixture
def admin_instance():
    admin = Admin("Admin Test", "Test Address", "admin@test.com", "1234567890", "adminuser", "adminpassword")
    return admin

# Define a fixture to create a temporary JSON file with admin data
@pytest.fixture
def admin_data_file(tmpdir, admin_instance):
    filename = os.path.join(tmpdir, 'admin_data.json')
    admin_data = [
        {
            "name": "Admin Test",
            "address": "Test Address",
            "email":" admin@test.com",
            "phone": "1234567890",
            "username": "adminuser",
            "password": "adminpassword",
        }
    ]
    with open(filename, 'w') as file:
        json.dump(admin_data, file)
    return filename


def test_admin_getter_methods(admin_instance):
    assert isinstance(admin_instance, Admin)
    assert admin_instance.name == "Admin Test"
    assert admin_instance.username == "adminuser"
    assert admin_instance.password == "adminpassword"

# =========== Test FrontDeskStaff class ============
# Define a fixture to create an Admin instance for testing
@pytest.fixture
def staff_instance():
    staff = FrontDeskStaff("Staff Test", "Test Address", "staff@test.com", "1234567899", "staffuser", "staffpassword")
    return staff

def test_staff_getter_methods(staff_instance):
    assert isinstance(staff_instance, FrontDeskStaff)
    assert staff_instance.name == "Staff Test"
    assert staff_instance.username == "staffuser"
    assert staff_instance.password == "staffpassword"


# Define a fixture to create a Customer instance for testing
@pytest.fixture
def customer_instance():
    customer = Customer("Customer Test", "Test Address", "customer@test.com", "1234567899", "customeruser", "customerpassword")
    return customer

# Define a fixture to create a sample booking for testing
@pytest.fixture
def sample_booking():
    customer = Customer("Customer Test", "Test Address", "customer@test.com", "1234567899", "customeruser", "customerpassword")
    movie = Movie("Sample Movie", "English", "Action", "USA", date(2023, 1, 1), 120, "Description")
    
    # Provide the missing arguments for the Screening class
    hall = CinemaHall("Hall 1", 100)  # Adjust the hall details as needed
    seats = []  # Provide a list of seats if needed
    screening = Screening(movie, date(2023, 1, 1), "Screen 1", date(2023, 1, 1), hall, seats)

    num_of_seats = 2
    selected_seats = ["A1", "A2"]
    created_on = date(2023, 1, 1)
    total_amount = 20.0
    status = "Pending"
    payment_method = 'Credit Card'

    return Booking(customer, movie, screening, num_of_seats, selected_seats, created_on, total_amount, status, payment_method)


def test_customer_getter_methods(customer_instance):
    assert isinstance(customer_instance, Customer)
    assert customer_instance.name == "Customer Test"
    assert customer_instance.address == "Test Address"
    assert customer_instance.username == "customeruser"
    assert customer_instance.password == "customerpassword"

def test_add_booking(customer_instance, sample_booking):
    # sample booking to the customer
    added = customer_instance.add_booking(sample_booking)

    # Check if the booking was successfully added
    assert added is True

    # Check if the booking is in the customer's bookings
    assert sample_booking in customer_instance.bookings()

def test_cancel_booking(customer_instance, sample_booking):
    # Add a sample booking to the customer
    customer_instance.add_booking(sample_booking)

    # Get the booking ID for cancellation
    booking_id = sample_booking.booking_id

    # Cancel the booking
    customer_instance.cancel_booking(booking_id)

    # Check if the booking status is 'Canceled'
    canceled_booking = customer_instance.find_booking(booking_id)
    assert canceled_booking is not None
    assert canceled_booking.status == 'Canceled'

def test_find_booking(customer_instance, sample_booking):
    # Add a sample booking to the customer
    customer_instance.add_booking(sample_booking)

    # Get the booking ID for finding
    booking_id = sample_booking.booking_id

    # Find the booking
    found_booking = customer_instance.find_booking(booking_id)

    # Check if the found booking is the same as the sample booking
    assert found_booking is not None
    assert found_booking == sample_booking

def test_add_notification(customer_instance):
    # Add a notification to the customer
    notification = "Your booking has been confirmed."
    customer_instance.add_notification(notification)

    # Check if the notification is in the customer's notifications
    assert notification in customer_instance.notifications

# Define a sample movie
@pytest.fixture
def sample_movie():
    return Movie("Sample Movie", "English", "Action", "USA", date(2023, 1, 1), 120, "Description")

# Define a sample screening
@pytest.fixture
def sample_screening(sample_movie):
    screening = Screening(
        sample_movie,
        date(2023, 1, 1),
        "Screen 1",
        "End Time",   # Provide a valid end time
        "Hall Name",  # Provide a valid hall name
        ["Seat 1", "Seat 2"]  # Provide a list of valid seats
    )
    return screening


# Test the creation of a Movie instance
def test_create_movie(sample_movie):
    assert sample_movie.title == "Sample Movie"
    assert sample_movie.language == "English"
    assert sample_movie.genre == "Action"
    assert sample_movie.country == "USA"
    assert sample_movie.release_date == date(2023, 1, 1)
    assert sample_movie.duration_in_mins == 120
    assert sample_movie.description == "Description"

# Test adding and retrieving screenings
def test_add_and_retrieve_screenings(sample_movie, sample_screening):
    # Add the screening to the movie
    sample_movie.add_screening(sample_screening)

    # Retrieve the added screening
    retrieved_screening = sample_movie.find_screening(sample_screening.screening_id)
    assert retrieved_screening is not None
    assert retrieved_screening.screening_id == sample_screening.screening_id
    assert retrieved_screening.screening_date == sample_screening.screening_date
    assert retrieved_screening.hall == sample_screening.hall
    assert retrieved_screening.seats == sample_screening.seats
    assert retrieved_screening.end_time == sample_screening.end_time


# Test deactivating a movie
def test_deactivate_movie(sample_movie):
    # Ensure the movie is initially active
    assert sample_movie.is_active is True

    # Deactivate the movie
    sample_movie.deactivate()

    # Check that the movie is now inactive
    assert sample_movie.is_active is False


def get_screening_date_list(self):
    """! Get a list of unique screening dates that are active and after the current date.
    @return (List[date]): A list of unique screening dates.
    """
    current_date = date.today()
    # Create a set of unique dates that are after the current date
    unique_dates = set()
    for screening in self.screenings:
        screening_date = screening.screening_date.strftime("%Y-%m-%d")  # Convert the date to a string
        screening_date = datetime.strptime(screening_date, "%Y-%m-%d").date()
        if screening_date >= current_date and screening.is_active:
            unique_dates.add(screening_date)
    # Convert to a list
    screening_date_list = sorted(list(unique_dates))
    return screening_date_list


@pytest.fixture
def sample_seat():
    return CinemaHallSeat(1, 1, False, 10.0)

def test_create_cinema_hall_seat(sample_seat):
    assert sample_seat.seat_number == 1
    assert sample_seat.row_number == 1
    assert sample_seat.is_reserved is False
    assert sample_seat.seat_price == 10.0

def test_seat_reservation(sample_seat):
    sample_seat.is_reserved = True
    assert sample_seat.is_reserved is True

def test_seat_price_update(sample_seat):
    sample_seat.seat_price = 15.0
    assert sample_seat.seat_price == 15.0

def test_seat_to_json(sample_seat):
    seat_json = sample_seat.to_json()
    assert seat_json["seat_number"] == 1
    assert seat_json["row_number"] == 1
    assert seat_json["is_reserved"] is False
    assert seat_json["seat_price"] == 10.0



def test_initialize_seats():
    # Create a CinemaHall instance with a capacity of 30
    hall = CinemaHall('hall name example', 30)
    
    # Test initializing seats for the cinema hall with a price of 10.0
    seat_price = 10.0
    seats = CinemaHallSeat.initialise_seats(hall, seat_price)

    # Check if the correct number of seats were initialized
    assert len(seats) == hall.capacity

    # Check if the first seat is available
    assert seats[0].is_reserved is False

    # Check if the price of the first seat matches the specified price
    assert seats[0].seat_price == seat_price

def test_cinema_hall_seat_string_representation(sample_seat):
    seat_string = str(sample_seat)
    assert "Seat 11 - Available - Price 10.0" in seat_string


# Define a sample CinemaHall
@pytest.fixture
def sample_hall():
    return CinemaHall("Hall A", 100)

# Define a sample CinemaHallSeat
@pytest.fixture
def sample_seat():
    return CinemaHallSeat(1, 1, False, 10.0)

# Define a sample Screening
@pytest.fixture
def sample_screening(sample_hall, sample_seat):
    return Screening(1, date(2023, 1, 1), "09:00 AM", "11:00 AM", sample_hall, [sample_seat])

# Test creation of a Screening instance
def test_create_screening(sample_screening):
    assert sample_screening.movie_id == 1
    assert sample_screening.screening_date == date(2023, 1, 1)
    assert sample_screening.start_time == "09:00 AM"
    assert sample_screening.end_time == "11:00 AM"


# Test setting the screening status to inactive
def test_set_screening_inactive(sample_screening):
    sample_screening.is_active = False
    assert sample_screening.is_active is False

# Test converting the screening details to a dictionary
def test_screening_to_dict(sample_screening):
    screening_dict = sample_screening.to_dict()
    assert screening_dict["screening_id"] == sample_screening.screening_id
    assert screening_dict["movie_id"] == sample_screening.movie_id
    assert screening_dict["screening_date"] == sample_screening.screening_date
    assert screening_dict["start_time"] == sample_screening.start_time
    assert screening_dict["end_time"] == sample_screening.end_time
    assert screening_dict["hall_name"] == sample_screening.hall.hall_name
    assert screening_dict["is_active"] == sample_screening.is_active

# Test finding a seat by identifier
def test_find_seat_by_identifier(sample_screening, sample_seat):
    seat = sample_screening.find_seat_by_identifier(1, 1)
    assert seat == sample_seat

# Test finding a seat by ID
def test_find_seat_by_id(sample_screening, sample_seat):
    seat = sample_screening.find_seat_by_id("11")
    assert seat == sample_seat

# Test string representation of a screening
def test_screening_string_representation(sample_screening):
    assert "Screening id:" in str(sample_screening)
    assert "Start Time:" in str(sample_screening)
    assert "End Time:" in str(sample_screening)
    assert "Hall:" in str(sample_screening)

# Define a sample coupon
@pytest.fixture
def sample_coupon():
    return Coupon("CODE123", 10.0, date(2023, 12, 31))

# Test creating a Coupon instance
def test_create_coupon(sample_coupon):
    assert sample_coupon.coupon_code == "CODE123"
    assert sample_coupon.discount_percentage == 10.0
    assert sample_coupon.expiration_date == date(2023, 12, 31)



# Define sample data
customer = Customer("John Doe", "123 Main St", "john@example.com", "123-456-7890", "john_doe", "password_here")
movie = Movie("Movie Title", "English", "Action", "USA", date(2023, 11, 5), 120, "A great action movie", True)
selected_seats = [CinemaHallSeat(1, 1, False, 10.0), CinemaHallSeat(1, 2, False, 10.0)]
created_on = date(2023, 12, 1)
total_amount = 20.0
hall = CinemaHall("Hall 1", 100)  # Replace 100 with the desired capacity
screening = Screening(1, "2023-12-01", "18:00", "20:00", hall, [], True)


# Create a Booking object
booking = Booking(customer, movie, screening, 2, selected_seats, created_on, total_amount, "active", "Credit Card")

# Test basic properties
def test_booking_properties():
    assert booking.customer == customer
    assert booking.movie == movie
    assert booking.screening == screening
    assert booking.num_of_seats == 2
    assert booking.selected_seats == selected_seats
    assert booking.created_on == created_on
    assert booking.total_amount == total_amount
    assert booking.status == "active"
    assert booking.payment is None
    assert booking.coupon is None

# Test changing status
def test_change_status():
    booking.status = "canceled"
    assert booking.status == "canceled"


# Test changing total amount
def test_change_total_amount():
    booking.total_amount = 15.0
    assert booking.total_amount == 15.0


if __name__ == '__main__':
    import pytest
    pytest.main()
