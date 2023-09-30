import sqlite3
from datetime import datetime

TAX_RATE = 0.07  # 7% tax, you can change this value

class CarRentalSystem:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            CarID TEXT PRIMARY KEY,
            CarName TEXT NOT NULL,
            DailyRate REAL NOT NULL,
            CustomRate REAL,
            RentedBy TEXT,
            NumberOfDays INTEGER,
            DateRented TEXT
        )
        """)

    def add_car(self, car_name, daily_rate):
        car_id = str(len(self.list_cars(all_cars=True)) + 1).zfill(5)
        self.cursor.execute("INSERT INTO cars (CarID, CarName, DailyRate) VALUES (?, ?, ?)", (car_id, car_name, daily_rate))
        self.conn.commit()

    def delete_car(self, car_id):
        self.cursor.execute("DELETE FROM cars WHERE CarID=?", (car_id,))
        self.conn.commit()

    def list_cars(self, all_cars=False):
        if all_cars:
            self.cursor.execute("SELECT * FROM cars")
        else:
            self.cursor.execute("SELECT * FROM cars WHERE RentedBy IS NULL")
        return self.cursor.fetchall()

    def rented_cars(self):
        self.cursor.execute("SELECT * FROM cars WHERE RentedBy IS NOT NULL")
        rented = self.cursor.fetchall()
        detailed_rented = []
        for car in rented:
            car_id, car_name, daily_rate, rented_by, days, date_rented = car
            total_cost = daily_rate * days
            total_cost_with_tax = total_cost + (total_cost * TAX_RATE)
            detailed_rented.append((car_id, car_name, rented_by, days, daily_rate, total_cost, total_cost_with_tax))
        return detailed_rented

    def return_car(self, car_id):
        self.cursor.execute("SELECT DailyRate, CustomRate, NumberOfDays FROM cars WHERE CarID=?", (car_id,))
        data = self.cursor.fetchone()
        daily_rate, custom_rate, days = data
        rate = custom_rate or daily_rate
        total_cost = rate * days
        print(f"Total cost for {days} days at ${rate}/day: ${total_cost}")
        self.cursor.execute("UPDATE cars SET RentedBy=NULL, NumberOfDays=NULL, DateRented=NULL, CustomRate=NULL WHERE CarID=?", (car_id,))
        self.conn.commit()

    def rented_cars(self):
        self.cursor.execute("SELECT * FROM cars WHERE RentedBy IS NOT NULL")
        rented = self.cursor.fetchall()
        detailed_rented = []
        for car in rented:
            car_id, car_name, daily_rate, custom_rate, rented_by, days, _ = car
            rate = custom_rate or daily_rate
            total_cost = rate * days
            total_cost_with_tax = total_cost + (total_cost * TAX_RATE)
            detailed_rented.append((car_id, car_name, rented_by, days, rate, total_cost, total_cost_with_tax))
        return detailed_rented

if __name__ == '__main__':
    rental_system = CarRentalSystem("rental_data.db")

    while True:
        print("\nOptions: \n1. List all cars \n2. Rent a car \n3. Return a car \n4. Add a car \n5. Delete a car \n6. Show rented cars \n7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            cars = rental_system.list_cars()
            for car in cars:
                print(car)
        elif choice == "2":
            cars = rental_system.list_cars()
            for index, car in enumerate(cars, 1):
                print(index, car)
            choice_index = int(input("Which car would you like to rent? Choose a number: ")) - 1
            car_id = cars[choice_index][0]
            customer_name = input("Enter your name: ")
            days = int(input("Enter number of days: "))
            rate_choice = input("Do you want to set a custom rate? (yes/no): ").lower()
            custom_rate = None
            if rate_choice == "yes":
                custom_rate = float(input("Enter custom rate: "))
            rental_system.rent_car(car_id, customer_name, days, custom_rate)
            print("Car rented successfully!")
        elif choice == "3":
            car_id = input("Enter car ID to return: ")
            rental_system.return_car(car_id)
            print("Car returned successfully!")
        elif choice == "4":
            car_name = input("Enter car name: ")
            daily_rate = float(input("Enter daily rate: "))
            rental_system.add_car(car_name, daily_rate)
            print("Car added successfully!")
        elif choice == "5":
            car_id = input("Enter car ID to delete: ")
            rental_system.delete_car(car_id)
            print("Car deleted successfully!")
        elif choice == "6":
            rented = rental_system.rented_cars()
            print("Rented Cars:")
            for car in rented:
                print(car)
        elif choice == "7":
            break
