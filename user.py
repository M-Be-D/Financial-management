import os
import json

class User:
    def __init__(self, users_list:str):
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
        self.users_path = users_list
        with open(users_list, "r") as u:
            self.users = json.load(u)
        self.usernames = self.users.keys()

    def create_user(self):
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
        
        def add_income(income):
            self.users[username]["income"].append(income)
            saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
            self.users[username]["saving"] = saving

        def add_expense(title, amount, category, description):
            self.users[username]["expanse"]["title"].append(title)
            self.users[username]["expanse"]["amount"].append(amount)
            self.users[username]["expanse"]["category"].append(category)
            self.users[username]["expanse"]["description"].append(description)
            self.users[username]["expanse"]["average"] = (sum(self.users[username]["expanse"]["amount"])/len(self.users[username]["expanse"]["amount"]))
            saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
            self.users[username]["saving"] = saving