# Movie_Ticket_Booking_System
A python Flask MVC program

validate password input

Customer:  
elaine  11112222
leowu   11112222

Admin
quentin 123

Front Desk Staff:
claire 123



when Admin cancel movie and cancel screening, movie and screening will be not deleted completed. as thus can cause id mismatch when reload system. is_active attribute included and when canceled, is_active will be set to False

for Pytest:
Search Methods (search_movie_title, search_movie_lang, search_movie_genre, search_movie_release_date) in Guest are tested. Those Search Methods are exactly same as Search Methods in Admin, Staff, Customer class.

how to run Pytest:
