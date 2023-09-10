import csv
import os
import datetime

CONFIG_FILE = "config.txt"
DATA_FILE = "data.csv"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None, [], []
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()
    password = lines[0].strip()
    expense_categories = lines[1].split(',')
    income_categories = lines[2].split(',')
    return password, expense_categories, income_categories

def save_config(password, expense_categories, income_categories):
    with open(CONFIG_FILE, 'w') as f:
        f.write(password + '\n')
        f.write(','.join(expense_categories) + '\n')
        f.write(','.join(income_categories))

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def add_expense_or_income(data, kind):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    amount = float(input("Enter amount: "))
    place = input("Enter place: ")
    category = input("Enter category: ")
    invoice_number = input("Enter invoice number: ")
    data.append([kind, date, amount, place, category, invoice_number])

def generate_report(data, start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.datetime.min
    if not end_date:
        end_date = datetime.datetime.max
    for row in data:
        date = datetime.datetime.strptime(row[1], "%Y-%m-%d")
        if start_date <= date <= end_date:
            print(row)

def main():
    password, expense_categories, income_categories = load_config()

    # If the user is new, prompt them to create a password
    if password is None:
        password = input("Welcome! Please create a password for your account: ")
        save_config(password, expense_categories, income_categories)

    entered_password = input("Enter password to login: ")
    while entered_password != password:
        print("Wrong password!")
        proceed = input("Forgot password? Do you want to reset? (yes/no): ")
        if proceed.lower() == 'yes':
            password = input("Please set a new password: ")
            save_config(password, expense_categories, income_categories)
            print("Password reset successful! Please login again.")
        entered_password = input("Enter password to login: ")

    data = load_data()

    while True:
        print("1. Add Expense")
        print("2. Add Income")
        print("3. Generate Monthly Report")
        print("4. Generate Report for a Period")
        print("5. Change Password")
        print("6. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            add_expense_or_income(data, "Expense")
        elif choice == 2:
            add_expense_or_income(data, "Income")
        elif choice == 3:
            now = datetime.datetime.now()
            start_date = datetime.datetime(now.year, now.month, 1)
            end_date = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(days=1)
            generate_report(data, start_date, end_date)
        elif choice == 4:
            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
            generate_report(data, start_date, end_date)
        elif choice == 5:
            new_password = input("Enter a new password: ")
            save_config(new_password, expense_categories, income_categories)
            print("Password changed successfully!")
        elif choice == 6:
            save_data(data)
            break

if __name__ == "__main__":
    main()
