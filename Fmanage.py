# start
from user import User
from admin import Admin
import banner
import random
import os
from time import sleep

# clean terminal
def clean():
    if os.name == "nt": # windows
        os.system('cls')
    else: # linux, mac os ,...
        os.system('clear')

clean() # clean terminal for start

def _banner():
    # banner
    banners = [banner.banner1, banner.banner2, banner.banner3]
    select_banner = random.choice(banners)
    select_banner()
    banner.connect()
if not os.path.exists('.manage/users.json'):
    _banner()
    user = User()
    print("""Welcome to MDkali Financial Accounting.
First you need to set up the admin user; set the admin password.""")
    print(25*"-")
    admin = Admin()

while os.path.exists('.manage/users.json'):
    clean()
    _banner()
    user = User()
    admin = Admin()
    # signin or signup
    print ("""
    1.sign in
    2.sign up
           
    0.exit
    """)
    choice = input('Choose one(0,1,2):')
    sleep(1)
    clean()
    _banner()
    if choice == '0':
        print("GoodBye!")
        exit()
    # login
    elif choice == "1":
        attempts = 1
        while True:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            login, role = user.login(username, password)
            if not login:
                print(f"\n***The username or password is incorrect! try again({attempts}/5)***")
                if attempts == 5:
                    print('There were many unsuccessful attempts.')
                    break
                attempts += 1
                continue
            else:
                sleep(1)
                # if role is user
                if role == 'user':
                    while True:
                        clean()
                        _banner()
                        print(f"user: {username}\n------------------------------------------------------------------------\n1. Record income\n2. Record expenses\n3. List expenses by category\n4. Total income and expenses and calculate savings\n5. Draw an expense chart\n6. Search expenses by title\n\n0.exit")
                        choice = input('What do you want to do? ')
                        if choice == "0":
                            print('GoodBye!')
                            exit()
                        elif choice == "1":
                            user.save_financial_data(username, s_income=True)
                            break
                        elif choice == "2":
                            user.save_financial_data(username, s_expense=True)
                            break
                        elif choice == "3":
                            categories = user.category(username)
                            while True:    
                                category = input(f'Enter the full name of your desired category (from the list=[{categories}]): ')
                                if category not in categories:
                                    print(f'{category} not exist in categories list.')
                                    continue
                                break
                            user.expense_list_by_category(username, category)
                            break
                        elif choice == "4":
                            user.sum(username)
                            break
                        elif choice == "5":
                            while True:
                                chart_type = input('What type of chart are you looking for (1.pie chart, 2.bar chart)? ')
                                if chart_type in ("1", "pie", "pie chart"):
                                    chart_type = 'pie'
                                    break
                                elif chart_type in ("2", "bar", "bar chart"):
                                    chart_type = "bar"
                                    break
                                else:
                                    print('Error: Choose one of the numbers 1 or 2')

                            user.chart(username, chart_type)
                            break
                        elif choice == "6":
                            titles = user.titles(username)
                            while True:
                                title = input(f'Enter the full name of your desired title (from the list=[{titles}]): ')
                                if title not in titles:
                                    print(f'{title} not exist in titles list.')
                                    continue
                                break
                            user.search(username, title)
                            break
                        else:
                            print('Error: Choose one of the numbers 1 or 2 or ... or 6')
                            sleep(2)
                            
                # if role is admin
                elif role == 'admin':
                    while True:
                        print("1.show all user\n2.fine user by username\n3.remove user\n4.add new user\n\n0.exit")
                        choice = input('What do you want to do? ')
                        if choice == "0":
                            print('GoodBye!')
                            exit()
                        elif choice == "1":
                            datas = admin.show_users()
                            while True:
                                n_user = input("Which user's information do you want (enter 0 to exit)? ")
                                if not n_user.isalnum():
                                    print(f'Error: Choose from 1 to {len(datas)}')
                                    continue
                                elif not (1 < int(n_user) < len(datas)):
                                    print(f'Choose from 1 to {len(datas)}')
                                    continue
                                else:
                                    print(datas[int(n_user)-1])
                                    break
                            break
                        elif choice == "2":
                            username = input("Enter the desired username: ")
                            admin.search_users(username)
                            break
                        elif choice == "3":
                            username = input("Enter the desired username: ")
                            status = False
                            admin.add_remove(username, add= status)
                            break
                        elif choice == "4":
                            username = input("Enter the desired username: ")
                            status = True
                            admin.add_remove(username, add= status)
                            break
                        else:
                            print('Error: Choose one of the numbers 1 or 2 or ... or 6')
                            continue
    # register
    elif choice == "2":
        user.create_user()
        sleep(2)