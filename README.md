# Movie Ticket Booking System

This is a Python Flask-based Movie Ticket Booking System.

## Login Credentials

### Customer
- Username: elaine
- Password: 11112222

- Username: leowu
- Password: 11112222

### Admin
- Username: quentin
- Password: 11112222

### Front Desk Staff
- Username: claire
- Password: 11112222

## Functionality

- When the Admin cancels a movie or screening, the `is_active` attribute is set to `False`. This prevents id mismatches when reloading the system.

## Pytest

- Search Methods (search_movie_title, search_movie_lang, search_movie_genre, search_movie_release_date) in the Guest class are tested. These Search Methods are the same as those in the Admin, Staff, and Customer classes.

## Running Pytest

To run Pytest, follow these steps:
1. Change to the `tests` directory.
2. Run the command: `python test_run.py`

