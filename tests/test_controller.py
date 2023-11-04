import pytest
from app.models import *
from app.controller import *

# Define sample data to use in tests
def create_sample_data(controller):
    # Create sample objects and add them to the controller
    admin1 = Admin("admin_name", "Admin address",  "admin1@example.com", "123456788", "admin1_username",  "admin1_password")
    front_desk1 = FrontDeskStaff("Front Desk 1", "Staff address", "123456789", "front_desk1@example.com", "front_desk1", "front_desk_password")
    customer1 = Customer( "Customer 1", "Customer address","1238956789", "customer1@example.com","customer1", "customer_password")
    movie1 = Movie("Movie 1", "English", "Action", "USA", date(2023, 11, 5), 120, "A great action movie", True)
    hall1 = CinemaHall("Hall 1", 100)
    coupon1 = Coupon("COUPON123", 10.0, date(2023, 12, 31))
    
    controller.add_admin(admin1)
    controller.add_front_desk_staff(front_desk1)
    controller.add_customer(customer1)
    controller.add_movie(movie1)
    controller.add_hall(hall1)
    controller.add_coupon(coupon1)

@pytest.fixture
def cinema_controller():
    controller = CinemaController()
    create_sample_data(controller)
    return controller

def test_get_all_admins(cinema_controller):
    admins = cinema_controller.all_admins
    assert len(admins) == 1  # One admin was added in the sample data

def test_get_all_front_desk_staffs(cinema_controller):
    front_desk_staffs = cinema_controller.all_front_desk_staffs
    assert len(front_desk_staffs) == 1  # One front desk staff was added in the sample data

def test_get_all_customers(cinema_controller):
    customers = cinema_controller.all_customers
    assert len(customers) == 1  # One customer was added in the sample data

def test_get_all_movies(cinema_controller):
    movies = cinema_controller.all_movies
    assert len(movies) == 1  # One movie was added in the sample data

def test_get_all_halls(cinema_controller):
    halls = cinema_controller.all_halls
    assert len(halls) == 1  # One hall was added in the sample data

def test_get_all_coupons(cinema_controller):
    coupons = cinema_controller.all_coupons
    assert len(coupons) == 1  # One coupon was added in the sample data


def test_find_admin(cinema_controller):
    # Positive test case: Find an existing admin
    existing_admin = cinema_controller.find_admin("admin1_username")
    assert existing_admin is not None
    assert existing_admin.username == "admin1_username"

    # Negative test case: Try to find a non-existing admin
    non_existing_admin = cinema_controller.find_admin("non_existing_admin")
    assert non_existing_admin is None

def test_find_staff(cinema_controller):
    # Positive test case: Find an existing staff
    existing_staff = cinema_controller.find_staff("front_desk1")
    assert existing_staff is not None
    assert existing_staff.username == "front_desk1"

    # Negative test case: Try to find a non-existing staff
    non_existing_staff = cinema_controller.find_staff("non_existing_staff")
    assert non_existing_staff is None

def test_find_customer(cinema_controller):
    # Positive test case: Find an existing customer
    existing_customer = cinema_controller.find_customer("customer1")
    assert existing_customer is not None
    assert existing_customer.username == "customer1"

    # Negative test case: Try to find a non-existing customer
    non_existing_customer = cinema_controller.find_customer("non_existing_customer")
    assert non_existing_customer is None


def test_find_hall(cinema_controller):
    # Positive test case: Find an existing hall
    existing_hall = cinema_controller.find_hall("Hall 1")
    assert existing_hall is not None
    assert existing_hall.hall_name == "Hall 1"

    # Negative test case: Try to find a non-existing hall
    non_existing_hall = cinema_controller.find_hall("Non-existing Hall")
    assert non_existing_hall is None

def test_find_coupon(cinema_controller):
    # Positive test case: Find an existing coupon
    existing_coupon = cinema_controller.find_coupon("COUPON123")
    assert existing_coupon is not None
    assert existing_coupon.coupon_code == "COUPON123"

    # Negative test case: Try to find a non-existing coupon
    non_existing_coupon = cinema_controller.find_coupon("Non-existing Coupon")
    assert non_existing_coupon is None


def test_get_language_list(cinema_controller):
    # Assuming you have a movie with the English language
    # Positive test case: Get a list of unique languages
    language_list = cinema_controller.get_language_list()
    assert "English" in language_list
    assert len(language_list) == 1  # Only one unique language

def test_get_genre_list(cinema_controller):
    # Assuming you have a movie with the Action genre
    # Positive test case: Get a list of unique genres
    genre_list = cinema_controller.get_genre_list()
    assert "Action" in genre_list
    assert len(genre_list) == 1  # Only one unique genre


def test_add_customer(cinema_controller):
    # Positive test case: Add a customer to the list
    new_customer = Customer( "Customer 1", "Customer address","1238956789", "customer1@example.com","customer1", "customer_password")
    cinema_controller.add_customer(new_customer)
    assert new_customer in cinema_controller.all_customers

def test_add_admin(cinema_controller):
    # Positive test case: Add an admin to the list
    new_admin = Admin("admin_name", "Admin address",  "admin1@example.com", "123456788", "admin1_username",  "admin1_password")
    cinema_controller.add_admin(new_admin)
    assert new_admin in cinema_controller.all_admins

def test_add_front_desk_staff(cinema_controller):
    # Positive test case: Add a front desk staff to the list
    new_front_desk_staff = FrontDeskStaff("Front Desk 1", "Staff address", "123456789", "front_desk1@example.com", "front_desk1", "front_desk_password")
    cinema_controller.add_front_desk_staff(new_front_desk_staff)
    assert new_front_desk_staff in cinema_controller.all_front_desk_staffs

def test_add_movie(cinema_controller):
    # Positive test case: Add a movie to the list
    new_movie = Movie("New Movie", "English", "Comedy", "USA", date(2023, 12, 1), 120, "A new comedy movie", True)
    cinema_controller.add_movie(new_movie)
    assert new_movie in cinema_controller.all_movies

def test_add_hall(cinema_controller):
    # Positive test case: Add a hall to the list
    new_hall = CinemaHall("New Hall", 50)
    cinema_controller.add_hall(new_hall)
    assert new_hall in cinema_controller.all_halls

def test_add_payment(cinema_controller):
    # Positive test case: Add a payment to the list
    new_payment = credit_card = CreditCard(1, 26.35, datetime(2023, 11, 3, 23, 10, 46), Coupon("GET15OFF", 15.0, datetime(2023, 12, 31)), "1111222233334444", "Card Type Here", datetime(2024, 12, 1), "E XU")
    cinema_controller.add_payment(new_payment)
    assert new_payment in cinema_controller.all_payments

def test_add_coupon(cinema_controller):
    # Positive test case: Add a coupon to the list
    new_coupon = Coupon("NEWCOUPON", 5.0, date(2023, 12, 31))
    cinema_controller.add_coupon(new_coupon)
    assert new_coupon in cinema_controller.all_coupons

def test_check_duplicate_username(cinema_controller):
    # Check for a username that exists
    existing_username = "customer1"
    assert cinema_controller.check_duplicate_username(existing_username) is True

    # Check for a username that doesn't exist
    non_existing_username = "nonexistingcustomer"
    assert cinema_controller.check_duplicate_username(non_existing_username) is False


def test_check_seat_availability(cinema_controller):
    # Create a sample booking with reserved seats
    selected_seats = [CinemaHallSeat(1, 1, True, 10.0), CinemaHallSeat(1, 2, False, 10.0)]
    screening = Screening(1, "2023-12-01", "18:00", "20:00", "Hall 1", [CinemaHallSeat(1, 1, True, 10.0)], True)
    booking = Booking(cinema_controller.all_customers[0], cinema_controller.all_movies[0], screening, 2, selected_seats, date(2023, 12, 1), 20.0, "active")

    # Check that seat availability is False
    assert cinema_controller.check_seat_availability(booking) is False

    # Create a sample booking with available seats
    selected_seats = [CinemaHallSeat(1, 3, False, 10.0), CinemaHallSeat(1, 4, False, 10.0)]
    booking = Booking(cinema_controller.all_customers[0], cinema_controller.all_movies[0], screening, 2, selected_seats, date(2023, 12, 1), 20.0, "active")

    # Check that seat availability is True
    assert cinema_controller.check_seat_availability(booking) is True

def test_customer_filter_movies():
    controller = CinemaController()
    # Create sample data for testing
    admin1 = Admin("admin_name", "Admin address", "admin1@example.com", "123456788", "admin1_username", "admin1_password")
    customer1 = Customer("Customer 1", "Customer address", "1238956789", "customer1@example.com", "customer1", "customer_password")
    movie1 = Movie("Movie 1", "English", "Action", "USA", date(2023, 11, 5), 120, "A great action movie", True)
    movie2 = Movie("Movie 2", "Spanish", "Comedy", "Spain", date(2023, 11, 6), 90, "A funny comedy movie", True)
    movie3 = Movie("Movie 3", "English", "Drama", "USA", date(2023, 11, 7), 110, "A dramatic movie", True)
    controller.add_admin(admin1)
    controller.add_customer(customer1)
    controller.add_movie(movie1)
    controller.add_movie(movie2)
    controller.add_movie(movie3)

    # Test filtering by title
    filtered_movies = controller.customer_filter_movies("Movie 1", "all", "all", None, None, customer1)
    assert len(filtered_movies) == 1
    assert movie1 in filtered_movies

    # Test filtering by language
    filtered_movies = controller.customer_filter_movies("Movie 1", "English", "all", None, None, customer1)
    assert len(filtered_movies) == 1
    assert movie1 in filtered_movies

    # Test filtering by genre
    filtered_movies = controller.customer_filter_movies("Movie 1", "English", "Action", None, None, customer1)
    assert len(filtered_movies) == 1
    assert movie1 in filtered_movies

    # Test filtering by date range
    filtered_movies = controller.customer_filter_movies("Movie 1", "all", "all", date(2023, 11, 5), date(2023, 11, 6), customer1)
    assert len(filtered_movies) == 1
    assert movie1 in filtered_movies

    # Test filtering with no matching criteria
    filtered_movies = controller.customer_filter_movies("Movie 1", "Spanish", "Drama", date(2023, 11, 8), date(2023, 11, 9), customer1)
    assert len(filtered_movies) == 0
