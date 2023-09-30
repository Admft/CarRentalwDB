Car Rental System
This Python script implements a basic car rental system using SQLite as a database. Users can add cars, list available cars, rent cars, return cars, and more.

Features
Add Car: You can add a new car to the system by specifying its name and daily rental rate.

Delete Car: Remove a car from the system by providing its unique CarID.

List Cars: You can list all cars available in the system or only the cars that are not currently rented.

Rent Car: Rent a car by selecting from the available cars, specifying the customer's name, number of days, and optionally setting a custom rate.

Return Car: Return a rented car by providing its CarID. The system calculates the total cost of the rental based on the rental rate and tax.

Show Rented Cars: Display a list of cars that are currently rented, along with detailed information about the rental.

Setup
Database Initialization: The script uses SQLite for data storage. When you run the script, it will create a database file named rental_data.db if it doesn't already exist.

Tax Rate: The default tax rate is set to 7%, but you can easily change this value by modifying the TAX_RATE variable in the script.

Usage
Run the script using a Python interpreter.

You'll be presented with a menu of options:

List all cars
Rent a car
Return a car
Add a car
Delete a car
Show rented cars
Exit
Choose an option by entering the corresponding number.

Follow the prompts to interact with the car rental system.

Example
Here's a simple example of using the script:

List all available cars.
Rent a car by specifying the car number, customer name, and rental duration.
Return the rented car when you're done.
Add or delete cars as needed.
Show rented cars to view active rentals.
Exit the script when you're finished.
Dependencies
Python 3.x
SQLite3 (Python Standard Library)
Author
Adam Moffat