import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
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
            car_id, car_name, daily_rate, custom_rate, rented_by, days, date_rented = car
            rate = custom_rate or daily_rate
            total_cost = rate * days
            total_cost_with_tax = total_cost + (total_cost * TAX_RATE)
            detailed_rented.append((car_id, car_name, rented_by, days, rate, total_cost, total_cost_with_tax))
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

    def rent_car(self, car_id, customer_name, days, custom_rate=None):
        date_rented = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("UPDATE cars SET RentedBy=?, NumberOfDays=?, DateRented=?, CustomRate=? WHERE CarID=?", (customer_name, days, date_rented, custom_rate, car_id))
        self.conn.commit()

    def format_cars_display(self, cars):
        return "\n".join(f"CarID: {car[0]}, Name: {car[1]}" for car in cars)

class CarRentalApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Rental System")
        
        self.rental_system = CarRentalSystem("rental_data.db")
        
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.master, text="Car Rental System", font=("Arial", 24))
        self.label.pack(pady=20)
        
        self.list_button = ttk.Button(self.master, text="List all cars", command=self.list_cars)
        self.list_button.pack(pady=10)

        self.rent_button = ttk.Button(self.master, text="Rent a car", command=self.rent_car)
        self.rent_button.pack(pady=10)

        self.return_button = ttk.Button(self.master, text="Return a car", command=self.return_car)
        self.return_button.pack(pady=10)

        self.add_button = ttk.Button(self.master, text="Add a car", command=self.add_car)
        self.add_button.pack(pady=10)

        self.delete_button = ttk.Button(self.master, text="Delete a car", command=self.delete_car)
        self.delete_button.pack(pady=10)

        self.show_rented_button = ttk.Button(self.master, text="Show rented cars", command=self.show_rented)
        self.show_rented_button.pack(pady=10)

    def list_cars(self):
        cars = self.rental_system.list_cars()
        cars_info = self.rental_system.format_cars_display(cars)
        messagebox.showinfo("Available Cars", cars_info)

    def rent_car(self):
        cars = self.rental_system.list_cars()
        cars_info = self.rental_system.format_cars_display(cars)
        messagebox.showinfo("Available Cars for Rent", cars_info)
        
        car_id = simpledialog.askstring("Rent a Car", "Enter CarID from above:")
        customer_name = simpledialog.askstring("Rent a Car", "Enter your name:")
        days = int(simpledialog.askstring("Rent a Car", "Enter number of days:"))
        rate_choice = simpledialog.askstring("Rent a Car", "Do you want to set a custom rate? (yes/no):").lower()
        
        custom_rate = None
        if rate_choice == "yes":
            custom_rate = float(simpledialog.askstring("Rent a Car", "Enter custom rate:"))
        
        self.rental_system.rent_car(car_id, customer_name, days, custom_rate)
        messagebox.showinfo("Success", "Car rented successfully!")

    def return_car(self):
        rented_cars = self.rental_system.rented_cars()
        rented_cars_info = self.rental_system.format_cars_display(rented_cars)
        messagebox.showinfo("Rented Cars", rented_cars_info)
        
        car_id = simpledialog.askstring("Return a Car", "Enter CarID from above:")
        self.rental_system.return_car(car_id)
        messagebox.showinfo("Success", "Car returned successfully!")

    def add_car(self):
        car_name = simpledialog.askstring("Add a Car", "Enter car name:")
        daily_rate = float(simpledialog.askstring("Add a Car", "Enter daily rate:"))
        self.rental_system.add_car(car_name, daily_rate)
        messagebox.showinfo("Success", "Car added successfully!")

    def delete_car(self):
        cars = self.rental_system.list_cars(all_cars=True)
        cars_info = self.rental_system.format_cars_display(cars)
        messagebox.showinfo("Cars in System", cars_info)
        
        car_id = simpledialog.askstring("Delete a Car", "Enter CarID from above:")
        self.rental_system.delete_car(car_id)
        messagebox.showinfo("Success", "Car deleted successfully!")

    def show_rented(self):
        rented = self.rental_system.rented_cars()
        if not rented:
            messagebox.showinfo("Rented Cars", "No cars are currently rented.")
            return
        rented_info = "\n".join(
            f"CarID: {r[0]}, Name: {r[1]}, Rented By: {r[2]}, Days: {r[3]}, Rate: ${r[4]:.2f}, Total: ${r[5]:.2f}, Total+Tax: ${r[6]:.2f}"
            for r in rented
        )
        messagebox.showinfo("Rented Cars", rented_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()
