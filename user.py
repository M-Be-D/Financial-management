# libraries
import os
import json
import hashlib
import matplotlib.pyplot as plt

# class 'User' for add new users
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
            "password": None,
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
            self.users = json.load(u)
        self.usernames = self.users.keys()

    def create_user(self):
        """
        To add new user
        """
        n = 1
        while n < 3:
            username = input("Please enter username: ")
            password = input("Enter password: ")

            if username in self.usernames:
                print(f"'{username}' already exists!")
                n += 1
                continue       

            elif password != input("Confirm your password: "):
                print("Passwords do not match. Please try again.")
                n += 1
                continue
            
            else:
                break

        self.users[username] = self.default_value
        self.users[username]['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest()
        with open(self.user_path, "w") as u:
            json.dump(self.users, u)
        print('User was created successfully.')
        print('From now on, you can sign in with this username.')

    def login(self, username, password: str):
        """
        To login
        """
        if username in self.usernames:
            if self.users[username]["password"] == hashlib.sha224(password.encode('utf-8')).hexdigest():
                role = self.users[username]['role']
                print(20*'-')
                print('* login successfully.')
                print(20*'-')
                return True, role
        return False, None

    def save_financial_data(self, username, s_income=False, s_expense=False):
        """
        To submit financial information
        """
        if s_income:
            income = input('enter your income: ')
            try:
                income = int(income)
                self._add_income(username, income)
            except:
                print('The income must be a number.')

        if s_expense:
            print('Enter the title, amount, category, and description.')
            while True:
                title = input('title: ')
                if title not in self.users[username]['expense']['title']:
                    break
                else:
                    print('Error: This title already exists.')

            amount = input('amount: ')
            try:
                amount = int(amount)
            except:
                print('The amount must be a number.')
                return

            category = input('category: ')
            description = input('description: ')
            self._add_expense(username, title, amount, category, description)

        with open(self.user_path, "w") as u:
            json.dump(self.users, u)

    def _add_income(self, username, income):
        """submit income"""
        self.users[username]["income"].append(income)
        expenses = self.users[username]["expense"]["amount"]
        self.users[username]["saving"] = sum(self.users[username]["income"]) - sum(expenses)

    def _add_expense(self, username, title, amount, category, description):
        """submit expense"""
        self.users[username]["expense"]["title"].append(title)
        self.users[username]["expense"]["amount"].append(amount)
        self.users[username]["expense"]["category"].append(category)
        self.users[username]["expense"]["description"].append(description)
        amounts = self.users[username]["expense"]["amount"]
        self.users[username]["expense"]["average"] = sum(amounts) / len(amounts)
        self.users[username]["saving"] = sum(self.users[username]["income"]) - sum(amounts)

    def expense_list_by_category(self, username, category):
        """
        To list expenses by category
        """
        amounts = [
            self.users[username]['expense']['amount'][i]
            for i, c in enumerate(self.users[username]['expense']['category'])
            if c == category
        ]
        print(amounts)

    def category(self, username):
        """
        To extract categories
        """
        return list(set(self.users[username]['expense']['category']))

    def sum(self, username):
        """
        To calculating total income, expenses, and savings
        """
        print(f"total income: {sum(self.users[username]['income'])}")
        print(f"total expenses: {sum(self.users[username]['expense']['amount'])}")
        print(f"savings: {self.users[username]['saving']}")

    def chart(self, username, chart_type):
        """
        To draw a diagram
        """
        titles = self.users[username]['expense']['title']
        expenses = self.users[username]['expense']['amount']

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

    def search(self, username, title):
        """
        To find the cost amount by title
        """
        if title not in self.users[username]['expense']['title']:
            print('This title not found.')
        else:
            idx = self.users[username]['expense']['title'].index(title)
            amount = self.users[username]['expense']['amount'][idx]
            print(f'Title: {title}, Cost amount: {amount}')

    def titles(self, username):
        """
        To extract titles
        """
        return self.users[username]['expense']['title']
