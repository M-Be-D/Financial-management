import os
import json
import hashlib
import matplotlib.pyplot as plt

class User:
    """
    # Config users
    * To add new user use 'create_user' method
    * To login use 'login' method
    * To submit financial information use 'save_financial_data' method
    * To list expenses by category use 'expense_list_by_category' method
    * To calculating total income, expenses, and savings use 'sum' method
    * To draw a diagram use 'chart' method
    * To find the cost amount by title use 'search' method
    """
    def __init__(self):
        self.default_value = {
            "role": "user",
            "password": '147ad31215fd55112ce613a7883902bb306aa35bba879cd2dbe500b9',
            "income": [],
            "expense": {
                "title": [],
                "amount": [],
                "category": [],
                "description": [],
                "average": 0
            },
            "saving": 0
        }

        if not os.path.exists('.manage'):
            os.mkdir('.manage')
            if os.name == "nt":
                os.system("attrib +h .manage")

        self.user_path = '.manage/users.json'
        if not os.path.isfile(self.user_path):
            with open(self.user_path, 'w') as file:
                json.dump({}, file)

        with open(self.user_path, "r") as u:
            try:
                self.users = json.load(u)
            except json.JSONDecodeError:
                self.users = {}

        self.usernames = list(self.users.keys())

    def save_users(self):
        """
        Save all user data to JSON file safely
        """
        try:
            with open(self.user_path, "w") as u:
                json.dump(self.users, u, indent=4)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def create_user(self):
        """
        To add new user
        """
        n = 1
        while n <= 3:
            username = input("Please enter username: ").strip()
            if not username:
                print("Username cannot be empty.")
                n += 1
                continue

            if username in self.usernames:
                print(f"'{username}' already exists!")
                n += 1
                continue

            password = input("Enter password: ")
            confirm = input("Confirm your password: ")

            if password != confirm:
                print("Passwords do not match. Please try again.")
                n += 1
                continue

            self.users[username] = self.default_value.copy()
            self.users[username]['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest()
            self.save_users()
            print("User was created successfully.")
            print("From now on, you can sign in with this username.")
            break

    def login(self, username, password):
        """
        To login
        """
        if username in self.usernames:
            hashed = hashlib.sha224(password.encode('utf-8')).hexdigest()
            if self.users[username]['password'] == hashed:
                role = self.users[username]['role']
                print(20*'-')
                print("* login successfully.")
                print(20*'-')
                return True, role
        return False, None

    def save_financial_data(self, username, s_income=False, s_expense=False):
        """
        To submit financial information
        """
        if s_income:
            income = input('enter your income: ').strip()
            if income.isdigit():
                self._add_income(username, int(income))
                self.save_users()
                print("Income recorded successfully.")
            else:
                print('The income must be a number.')

        if s_expense:
            print('Enter the title, amount, category, and description.')
            while True:
                title = input('title: ').strip()
                if title and title not in self.users[username]['expense']['title']:
                    break
                print('Error: This title is empty or already exists.')

            amount = input('amount: ').strip()
            if not amount.isdigit():
                print('The amount must be a number.')
                return
            amount = int(amount)

            category = input('category: ').strip()
            if not category:
                print("Category cannot be empty.")
                return

            description = input('description: ').strip()
            # description can be empty

            self._add_expense(username, title, amount, category, description)
            self.save_users()
            print("Expense recorded successfully.")

    def _add_income(self, username, income):
        self.users[username]["income"].append(income)
        saving = sum(self.users[username]["income"]) - sum(self.users[username]["expense"]["amount"])
        self.users[username]["saving"] = saving

    def _add_expense(self, username, title, amount, category, description):
        self.users[username]["expense"]["title"].append(title)
        self.users[username]["expense"]["amount"].append(amount)
        self.users[username]["expense"]["category"].append(category)
        self.users[username]["expense"]["description"].append(description)
        amounts = self.users[username]["expense"]["amount"]
        self.users[username]["expense"]["average"] = sum(amounts) / len(amounts) if amounts else 0
        saving = sum(self.users[username]["income"]) - sum(amounts)
        self.users[username]["saving"] = saving

    def expense_list_by_category(self, username, category):
        indexes = [i for i, c in enumerate(self.users[username]['expense']['category']) if c == category]
        expenses = [self.users[username]['expense']['amount'][i] for i in indexes]
        if not expenses:
            print(f"No expenses found in category '{category}'.")
        else:
            print(f"Expenses in category '{category}': {expenses}")

    def category(self, username):
        categories = self.users[username]['expense']['category']
        return list(set(categories)) if categories else []

    def sum(self, username):
        total_income = sum(self.users[username]['income'])
        total_expenses = sum(self.users[username]['expense']['amount'])
        savings = self.users[username]['saving']

        print(f"total income: {total_income}")
        print(f"total expenses: {total_expenses}")
        print(f"savings: {savings}")

    def chart(self, username, chart_type):
        titles = self.users[username]['expense']['title']
        expenses = self.users[username]['expense']['amount']

        if not titles or not expenses:
            print("No expense data to show chart.")
            return

        try:
            if chart_type == 'bar':
                plt.bar(titles, expenses)
                plt.title('Cost distribution')
                plt.xlabel('title')
                plt.ylabel('Cost amount')
                plt.show()
            elif chart_type == 'pie':
                plt.pie(expenses, labels=titles, autopct='%1.1f%%', startangle=0)
                plt.title('Cost distribution')
                plt.axis('equal')
                plt.show()
        except Exception as e:
            print(f"Error showing chart: {e}")

    def search(self, username, title):
        if title not in self.users[username]['expense']['title']:
            print('This title not found.')
        else:
            idx = self.users[username]['expense']['title'].index(title)
            amount = self.users[username]['expense']['amount'][idx]
            print(f'Title: {title}, Cost amount: {amount}')

    def titles(self, username):
        return self.users[username]['expense']['title']
