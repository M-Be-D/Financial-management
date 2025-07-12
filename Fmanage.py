# start
from user import User
from admin import Admin
import banner
import random
import os
from time import sleep

# clean terminal
def clean():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

clean()

def _banner():
    banners = [banner.banner1, banner.banner2, banner.banner3]
    select_banner = random.choice(banners)
    select_banner()
    banner.connect()

if not os.path.exists('.manage/users.json'):
    _banner()
    user = User()
    print("""Welcome to MDkali Financial Accounting.
First you need to set up the admin user; set the admin password.""")
    print(72*"-")
    admin = Admin()

while os.path.exists('.manage/users.json'):
    clean()
    _banner()
    user = User()
    admin = Admin()

    print ("""
    1. Sign in
    2. Sign up
    0. Exit
    """)
    choice = input('Choose one (0,1,2): ').strip()
    sleep(1)
    clean()
    _banner()

    if choice == '0':
        confirm = input("Are you sure you want to exit? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            print("GoodBye!")
            break
        else:
            continue

    elif choice == "1":
        attempts = 1
        while True:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            login, role = user.login(username, password)
            if not login:
                print(f"\n***The username or password is incorrect! try again ({attempts}/5)***")
                if attempts == 5:
                    print('There were too many unsuccessful attempts.')
                    break
                attempts += 1
                continue
            else:
                sleep(1)
                # User dashboard
                if role == 'user':
                    while True:
                        clean()
                        _banner()
                        print(f"user: {username}\n" + "-"*72)
                        print("1. Record income")
                        print("2. Record expenses")
                        print("3. List expenses by category")
                        print("4. Total income and expenses and calculate savings")
                        print("5. Draw an expense chart")
                        print("6. Search expenses by title")
                        print("0. Logout")
                        choice = input('Choose an option: ').strip()

                        if choice == "0":
                            break
                        elif choice == "1":
                            user.save_financial_data(username, s_income=True)
                        elif choice == "2":
                            user.save_financial_data(username, s_expense=True)
                        elif choice == "3":
                            categories = user.category(username)
                            while True:
                                category = input(f'Enter category (from list={categories}): ')
                                if category not in categories:
                                    print(f'{category} not found in the list.')
                                    continue
                                break
                            user.expense_list_by_category(username, category)
                        elif choice == "4":
                            user.sum(username)
                        elif choice == "5":
                            while True:
                                chart_type = input('Chart type (1. pie, 2. bar): ')
                                if chart_type in ("1", "pie", "pie chart"):
                                    user.chart(username, 'pie')
                                    break
                                elif chart_type in ("2", "bar", "bar chart"):
                                    user.chart(username, 'bar')
                                    break
                                else:
                                    print('Choose 1 or 2')
                        elif choice == "6":
                            titles = user.titles(username)
                            while True:
                                title = input(f'Enter title (from list={titles}): ')
                                if title not in titles:
                                    print(f'{title} not found.')
                                    continue
                                break
                            user.search(username, title)
                        else:
                            print('Invalid option.')
                            sleep(2)

                # Admin dashboard
                elif role == 'admin':
                    while True:
                        clean()
                        _banner()
                        print("1. Show all users")
                        print("2. Find user by username")
                        print("3. Remove user")
                        print("4. Add new user")
                        print("0. Logout")
                        choice = input('Choose an option: ').strip()

                        if choice == "0":
                            break
                        elif choice == "1":
                            datas = admin.show_users()
                            while True:
                                n_user = input("Enter user number to view (0 to exit): ").strip()
                                if n_user == "0":
                                    break
                                try:
                                    idx = int(n_user)
                                    if 1 <= idx <= len(datas):
                                        print(datas[idx - 1])
                                    else:
                                        print(f"Choose from 1 to {len(datas)}")
                                except:
                                    print("Enter a valid number.")
                        elif choice == "2":
                            username = input("Enter username: ")
                            admin.search_users(username)
                        elif choice == "3":
                            username = input("Enter username to remove: ")
                            admin.add_remove(username, add=False)
                        elif choice == "4":
                            username = input("Enter new username to add: ")
                            admin.add_remove(username, add=True)
                        else:
                            print('Invalid option.')
                            sleep(2)

    elif choice == "2":
        user.create_user()
        sleep(2)
