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
            self.users['admin'] = self.default_value.copy()
            confirm = input("Confirm your password: ")
            if password == confirm:
                self.users['admin']['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest()
            else:
                print('The passwords do not match.')
                if os.path.exists(self.user_path):
                    os.remove(self.user_path)
                return
            self.users['admin']["role"] = 'admin'
            self.save_users()
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')

    def show_users(self):
        """
        Show all users with their number
        """
        n = 1
        datas = []
        for username, data in self.users.items():
            print(f'{n}.{username}')
            datas.append(f'{username}: {data}')
            n += 1
        input("\nPress Enter to continue...")
        return datas

    def search_users(self, username):
        """
        Find user by username
        """
        if username not in self.usernames:
            print(f'{username} not exist.')
        else:
            print(f'{username}\n{self.users[username]}')
        input("\nPress Enter to continue...")

    def add_remove(self, username, add: bool):
        """
        To add or remove user
        - add_remove ('username',True) --> add new user
        - add_remove ('username',False) --> remove user
        """
        if add:
            if username not in self.usernames:
                self.users[username] = self.default_value.copy()
                self.save_users()
                print(f"User '{username}' added.")
            else:
                print(f"'{username}' already exists!")
        else:
            if username not in self.usernames:
                print(f"User '{username}' does not exist.")
            else:
                check_ok = input("Are you sure you want to delete it (yes/no)? ").lower()
                if check_ok in ('yes', 'y'):
                    try:
                        self.users.pop(username)
                        self.save_users()
                        print(f"User '{username}' deleted.")
                    except Exception as e:
                        print(f"Error deleting user: {e}")
                else:
                    print("The user deletion operation was canceled.")
        input("\nPress Enter to continue...")

    def save_users(self):
        """
        Save all user data to JSON file
        """
        with open(self.user_path, "w") as u:
            json.dump(self.users, u, indent=4)
