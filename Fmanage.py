from user import User
from admin import Admin
import banner
import random
import os
from time import sleep

def clean():
    """
    Clear terminal screen
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def _banner():
    """
    Display random banner and connect message
    """
    banners = [banner.banner1, banner.banner2, banner.banner3]
    random.choice(banners)()
    banner.connect()

def main():
    """
    Main entry function
    """
    # Initialize user and admin only once
    if not os.path.exists('.manage/users.json'):
        clean()
        _banner()
        user_obj = User()
        print("""Welcome to MDkali Financial Accounting.
First you need to set up the admin user; set the admin password.""")
        print(72*"-")
        admin_obj = Admin()

    while True:
        clean()
        _banner()
        user_obj = User()
        admin_obj = Admin()
        print("""
        1.sign in
        2.sign up
        0.exit
        """)
        choice = input('Choose one(0,1,2):').strip()
        if choice == '0':
            print("GoodBye!")
            break
        elif choice == '1':
            username, role = signin(user_obj)
            if username:
                if role == 'user':
                    user_menu(user_obj, username)
                elif role == 'admin':
                    admin_menu(admin_obj)
        elif choice == '2':
            user_obj.create_user()
            sleep(2)

def signin(user_obj):
    attempts = 1
    while attempts <= 5:
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ').strip()
        login, role = user_obj.login(username, password)
        if login:
            return username, role
        else:
            print(f"\n***The username or password is incorrect! try again({attempts}/5)***")
            attempts += 1
            sleep(1)
    print('There were many unsuccessful attempts.')
    sleep(2)
    return None, None

def user_menu(user_obj, username):
    while True:
        clean()
        _banner()
        print(f"user: {username}\n{'-'*72}\n"
              "1. Record income\n"
              "2. Record expenses\n"
              "3. List expenses by category\n"
              "4. Total income and expenses and calculate savings\n"
              "5. Draw an expense chart\n"
              "6. Search expenses by title\n"
              "0. Logout\n")
        choice = input('What do you want to do? ').strip()
        if choice == '0':
            print("Logging out...")
            sleep(1)
            break
        elif choice == '1':
            user_obj.save_financial_data(username, s_income=True)
            input("\nPress Enter to continue...")
        elif choice == '2':
            user_obj.save_financial_data(username, s_expense=True)
            input("\nPress Enter to continue...")
        elif choice == '3':
            categories = user_obj.category(username)
            if not categories:
                print("No categories found.")
                input("\nPress Enter to continue...")
                continue
            while True:
                category = input(f'Enter the full name of your desired category (from the list=[{categories}]): ').strip()
                if category not in categories:
                    print(f'{category} not exist in categories list.')
                else:
                    break
            user_obj.expense_list_by_category(username, category)
            input("\nPress Enter to continue...")
        elif choice == '4':
            user_obj.sum(username)
            input("\nPress Enter to continue...")
        elif choice == '5':
            while True:
                chart_type = input('What type of chart are you looking for (1.pie chart, 2.bar chart)? ').strip().lower()
                if chart_type in ('1', 'pie', 'pie chart'):
                    chart_type = 'pie'
                    break
                elif chart_type in ('2', 'bar', 'bar chart'):
                    chart_type = 'bar'
                    break
                else:
                    print('Error: Choose one of the numbers 1 or 2')
            user_obj.chart(username, chart_type)
            input("\nPress Enter to continue...")
        elif choice == '6':
            titles = user_obj.titles(username)
            if not titles:
                print("No titles found.")
                input("\nPress Enter to continue...")
                continue
            while True:
                title = input(f'Enter the full name of your desired title (from the list=[{titles}]): ').strip()
                if title not in titles:
                    print(f'{title} not exist in titles list.')
                else:
                    break
            user_obj.search(username, title)
            input("\nPress Enter to continue...")
        else:
            print("Error: Choose a valid option")
            sleep(2)

def admin_menu(admin_obj):
    while True:
        clean()
        _banner()
        print("1.show all users\n2.find user by username\n3.remove user\n4.add new user\n0.logout\n")
        choice = input('What do you want to do? ').strip()
        if choice == '0':
            print("Logging out...")
            sleep(1)
            break
        elif choice == '1':
            datas = admin_obj.show_users()
            if not datas:
                print("No users found.")
                input("\nPress Enter to continue...")
                continue
            while True:
                n_user = input(f"Which user's information do you want (enter number 1 to {len(datas)} or 0 to exit)? ").strip()
                if n_user == '0':
                    break
                if not n_user.isdigit():
                    print(f'Error: Choose from 1 to {len(datas)} or 0 to exit')
                    continue
                n_user_int = int(n_user)
                if not (1 <= n_user_int <= len(datas)):
                    print(f'Choose from 1 to {len(datas)}')
                    continue
                username = datas[n_user_int - 1]
                admin_obj.search_users(username)
                break
        elif choice == '2':
            username = input("Enter the desired username: ").strip()
            admin_obj.search_users(username)
        elif choice == '3':
            username = input("Enter the desired username: ").strip()
            admin_obj.add_remove(username, add=False)
        elif choice == '4':
            username = input("Enter the desired username: ").strip()
            admin_obj.add_remove(username, add=True)
        else:
            print("Error: Choose a valid option")
            sleep(2)

if __name__ == "__main__":
    main()
