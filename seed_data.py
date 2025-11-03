# backend/seed_data.py
from database import SessionLocal, Customer, init_db
import random

init_db()
db = SessionLocal()

# Some sample names and countries to randomize
names = [
    "Ramya", "Arun", "Meena", "John", "Kavya", "Suresh", "Priya", "Ravi", "Divya",
    "Anil", "Lakshmi", "Rahul", "Sneha", "Karthik", "Nisha", "Deepak", "Swathi",
    "Arjun", "Gopi", "Pooja", "Vikram", "Asha", "Manoj", "Shreya", "Kiran",
    "Saranya", "Bharath", "Neha", "Ajay", "Ishita", "Varun", "Aarav", "Keerthi",
    "Harsha", "Teja", "Rajesh", "Sindhu", "Vani", "Krishna", "Devi", "Monika",
    "Balaji", "Naveen", "Lavanya", "Vignesh", "Sanjay", "Chitra", "Gautam",
    "Pavan", "Yamini", "Bhavana"
]

countries = ["India", "USA", "UK", "Germany", "France", "Australia", "Canada", "Japan", "Singapore", "UAE"]

customers = []
for i in range(50):
    name = names[i % len(names)]
    email = f"{name.lower()}{i}@example.com"
    country = random.choice(countries)
    total_purchases = round(random.uniform(100, 5000), 2)
    customers.append(Customer(name=name, email=email, country=country, total_purchases=total_purchases))

db.add_all(customers)
db.commit()
db.close()

print("✅ 50 sample customer records inserted successfully!")



