# use User class from user.py
from user import User
import hashlib
import json
import os

class Admin(User):
    """
    # Config admin
    * Show all users with 'show_users' method
    * Fine user by username with 'search_users'  method
    * To add or remove user use 'add_remove' method
    """
    def __init__(self):
        super().__init__()
        if 'admin' not in self.usernames:
            password = input('enter admin password: ')
            self.users['admin'] = self.default_value
            confirm = input("Confirm your password: ")
            if password == confirm:
                self.users['admin']['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest()
            else:
                print('The passwords do not match.')
                os.remove(self.user_path)
                return
            self.users['admin']["role"] = 'admin'
            with open(self.user_path, "w") as u:
                json.dump(self.users, u)
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')

    def show_users(self):
        """
        show all users
        """
        n = 1
        datas = []
        for username, data in self.users.items():
            print(f'{n}.{username}')
            datas.append(f'{username}: {data}')
            n += 1
        return datas

    def search_users(self, username):
        """
        fine user by username
        """
        if username not in self.usernames:
            print(f'{username} not exist.')
        else:
            print(f'{username}\n{self.users[username]}')

    def add_remove(self, username, add: bool):
        """
        To add or remove user
        - add_remove ('username',True) --> add new user
        - add_remove ('username',False) --> remove user
        """
        if add:
            if username not in self.usernames:
                self.users[username] = self.default_value
                with open(self.user_path, "w") as u:
                    json.dump(self.users, u)
            else:
                print(f"'{username}' already exists!")
        else:
            if username not in self.usernames:
                print(f"User '{username}' does not exist.")
                return
            check_ok = input("Are you sure you want to delete it (yes/no)? ").lower()
            if check_ok in ('yes', "y"):
                try:
                    self.users.pop(username)
                    with open(self.user_path, "w") as u:
                        json.dump(self.users, u)
                except:
                    print("Something went wrong while removing the user.")
            elif check_ok in ('no', 'n'):
                print('The user deletion operation was canceled.')
