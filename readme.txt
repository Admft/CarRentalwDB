Car Rental System
The Car Rental System is a Python-based application using SQLite for data storage and tkinter for GUI. It allows users to rent, return, add, or delete cars and view current rentals.

Features
List all cars.
Rent a car.
Return a rented car.
Add a new car to the system.
Delete a car from the system.
Display currently rented cars.
Setup
Requirements
Python
SQLite
tkinter
Running the application
Make sure you have Python and SQLite installed.
Clone or download the source code.
Navigate to the directory containing the code.
Run the application with:
php
Copy code
python <filename>.py
Replace <filename>.py with the name you've saved the code as.

How to use
List all cars: Displays a list of all cars in the system.
Rent a car: Allows a user to rent an available car. The user will be asked for the CarID, their name, number of days, and an optional custom rate.
Return a car: Enables a user to return a rented car. The user will be asked for the CarID of the car they're returning.
Add a car: Adds a new car to the system. The user will be prompted for the car name and daily rate.
Delete a car: Removes a car from the system. The user will be asked for the CarID of the car they wish to delete.
Show rented cars: Displays a list of cars that are currently rented.
Design
The application is designed with two main classes:

CarRentalSystem: Manages the database operations such as adding, deleting, renting, and returning cars.
CarRentalApp: Manages the GUI of the application and interacts with the CarRentalSystem.
Database
The application uses an SQLite database (rental_data.db) with a table named cars to store all the information about the cars.

Schema:
CarID: Unique identifier for each car.
CarName: Name of the car.
DailyRate: Standard daily rate for renting the car.
CustomRate: Custom rate (if set during renting).
RentedBy: Name of the person who rented the car (if rented).
NumberOfDays: Number of days the car has been rented for.
DateRented: Date the car was rented.
Customizations
Tax Rate: The tax rate is set as a constant TAX_RATE at 7%. You can adjust this rate by changing the value of this constant.

Author: Adam Moffat