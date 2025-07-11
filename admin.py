# use User class from user.py
from user import User
import hashlib
import json

class Admin(User):
    """
    config admin
    """
    def __init__(self):
        super().__init__()
        if 'admin' not in self.usernames:
            password = input('enter admin password: ')
            self.users['admin'] = self.default_value
            if password == input("Confirm your password: "):
                self.users['admin']['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest() # save password hash
            with open(self.users_path, "w") as u:
                json.dump(self.users, u)
                u.close()
    
    def show_users(self):
        """
        show all users
        """
        print(self.users)

    def search_users(self, username):
        """
        fine user by username
        """
        if username not in self.usernames:
            print(f'{username} not exist.')
        else:
            print(f'{username}\n{self.users[username]}')
    
    def add_remove(self, username, add:bool):
        """
        To add or remove user
        """
        if add:
            if username not in self.usernames:
                self.users[username] = self.default_value
                with open(self.users_path, "w") as u:
                    json.dump(self.users, u)
                    u.close()
            else:
                print(f"'{username}' already exists!")
        elif not add:
            check_ok = input("Are you sure you want to delete it (yes/no)? ").lower()
            if check_ok in ('yes', "y"):
                self.users.pop(username)
                with open(self.users_path, "w") as u:
                    json.dump(self.users, u)
                    u.close()
            elif check_ok in ('no', 'n'):
                print('The user deletion operation was canceled.')