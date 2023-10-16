from .models import *


class CinemaController:
    def __init__(self):
        self.__customers = []

    @property
    def all_customers(self):
        return self.__customers
    
    
    def find_customer(self, username):
        for customer in self.__customers:
            if customer.username == username:
                return customer
        return None


    def add_customer(self, customer):
        self.__customers.append(customer)
    
 
    def register_customer(self, name, address, email, phone, username, hashed_password) -> bool:
        # Check if the username already exists
        if self.find_customer(username):
            return False
        new_customer = Customer(name, address, email, phone, username, hashed_password)
        self.add_customer(new_customer)
        with open('app/database/customers.txt', 'a') as file:
            file.write(f"{new_customer.name},{new_customer.address},{new_customer.email},{new_customer.phone},{new_customer.username},{new_customer.password}\n")
        return True


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


    
    def load_database(self):
        self.add_customers_from_file('app/database/customers.txt')
