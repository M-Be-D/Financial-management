# libraries
import os
import json

# class 'User' for add new users
class User:
    """
    # Config users
    * To add new user use 'create_user' method
    * To login use 'login' method
    * To submit financial information use 'save_financial_data' method
    """
    def __init__(self, users_list:str):
        self.default_value = {
            "role": "user",
            "password": None,
            "income": [],
            "expense": {
                "title": [], # عنوان
                "amount": [], # مبلغ
                "category": [], # دسته بندی
                "description": [], # توضیحات
                "average": 0 
            },
            "saving": 0 # پس‌انداز
        }
        self.users_path = users_list
        with open(users_list, "r") as u:
            self.users = json.load(u)
        self.usernames = self.users.keys()

    def create_user(self):
        """
        To add new user
        """
        username = input("Please enter username: ")
        password = input("Enter password: ")
        
        if username in self.usernames:
            print(f"'{username}' already exists!")
            raise Exception("user_error")        
        
        elif password != input("Confirm your password: "):
            print("Passwords do not match. Please try again.")
            raise Exception("pass_error")

        else:
            self.users[username] = self.default_value
            with open(self.users_path, "w") as u:
                json.dump(self.users, u)
                u.close()
        
    def login(self, username, password):
        """
        To login
        """
        if username in self.usernames:
            if self.users[username]["password"] == password:
                return True
            else:
                print("The password is incorrect!")
                return False
        else:
            print("There is no user with this username!")
            return False
        
    def save_financial_data(self, username):
        """
        To submit financial information
        """
        # submit income
        def add_income(income):
            self.users[username]["income"].append(income)
            saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
            self.users[username]["saving"] = saving

        # submit expense
        def add_expense(title, amount, category, description):
            self.users[username]["expanse"]["title"].append(title)
            self.users[username]["expanse"]["amount"].append(amount)
            self.users[username]["expanse"]["category"].append(category)
            self.users[username]["expanse"]["description"].append(description)
            self.users[username]["expanse"]["average"] = (sum(self.users[username]["expanse"]["amount"])/len(self.users[username]["expanse"]["amount"]))
            saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
            self.users[username]["saving"] = saving