import os
import json

class User:
    def __init__(self, users_list:str):
        self.default_value = {
            "role": "user",
            "password": None,
            "income": [],
            "expense": {
                "Title": [],
                "Amount": [],
                "Category": [],
                "Description": []
            },
            "savings": []
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
            User(self.users_path)
        
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