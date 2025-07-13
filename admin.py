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
            password = input('enter admin password: ').strip()
            confirm = input("Confirm your password: ").strip()
            if not password:
                print("Password cannot be empty.")
                return
            if password == confirm:
                self.users['admin'] = self.default_value.copy()
                self.users['admin']['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest()
                self.users['admin']["role"] = 'admin'
                self.save_users()
                if os.name == "nt":
                    os.system('cls')
                else:
                    os.system('clear')
            else:
                print('The passwords do not match.')
                # Do not delete users file, just return
                return

    def save_users(self):
        try:
            with open(self.user_path, "w") as u:
                json.dump(self.users, u, indent=4)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def show_users(self):
        n = 1
        datas = []
        for username in self.users:
            print(f'{n}. {username}')
            datas.append(username)
            n += 1
        return datas

    def search_users(self, username):
        if username not in self.usernames:
            print(f'{username} not exist.')
        else:
            user_data = self.users[username].copy()
            # Hide password hash for display
            user_data['password'] = "********"
            print(f'{username}\n{user_data}')
        input("\nPress Enter to continue...")

    def add_remove(self, username, add: bool):
        if add:
            if not username.strip():
                print("Username cannot be empty.")
                input("\nPress Enter to continue...")
                return
            if username in self.usernames:
                print(f"'{username}' already exists!")
            else:
                self.users[username] = self.default_value.copy()
                self.save_users()
                print(f"User '{username}' added.")
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
