# libraries
import os
import json
import hashlib

# class 'User' for add new users
class User:
    """
    # Config users
    * To add new user use 'create_user' method
    * To login use 'login' method
    * To submit financial information use 'save_financial_data' method
    * To list expenses by category use 'expense_list_by_category' method
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
        n = 1
        while n < 3:
            username = input("Please enter username: ")
            password = input("Enter password: ")

            if username in self.usernames:
                print(f"'{username}' already exists!")
                n += 1
                continue       

            elif password != input("Confirm your password: "):
                print("Passwords do not match. Please try again.")
                n += 1
                continue
            
            else:
                break
    
        self.users[username] = self.default_value
        self.users[username]['password'] = hashlib.sha224(password.encode('utf-8')).hexdigest() # save password hash
        with open(self.users_path, "w") as u:
            json.dump(self.users, u)
            u.close()
        
    def login(self, username, password:str):
        """
        To login
        """
        if username in self.usernames:
            if self.users[username]["password"] == hashlib.sha224(password.encode('utf-8')).hexdigest():
                return True
            else:
                print("The password is incorrect!")
                return False
        else:
            print(f"{username} is not exist.")
            return False
        
    def save_financial_data(self, username, s_income=False, s_expense=False):
        """
        To submit financial information
        """
        if s_income:
            income = input('enter your income: ')
            self._add_income(username, income)

        if s_expense:
            print('Enter the title, amount, category, and description.')
            title = input('title: ')
            amount = input('amount: ')
            category = input('category: ')
            description = input('description: ')
            self._add_expense(username, title, amount, category, description)
    
    def _add_income(self, username, income):
        """submit income"""
        self.users[username]["income"].append(income)
        saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
        self.users[username]["saving"] = saving
    
    def _add_expense(self, username, title, amount, category, description):
        """submit expense"""
        # submit expense data
        self.users[username]["expanse"]["title"].append(title)
        self.users[username]["expanse"]["amount"].append(amount)
        self.users[username]["expanse"]["category"].append(category)
        self.users[username]["expanse"]["description"].append(description)
        self.users[username]["expanse"]["average"] = (sum(self.users[username]["expanse"]["amount"])/len(self.users[username]["expanse"]["amount"]))
        # Calculate savings
        saving = sum(self.users[username]["income"]) - sum(self.users[username]["expanse"]["amount"])
        self.users[username]["saving"] = saving

    def expense_list_by_category(self, username, category):
        """
        To list expenses by category
        """
        index_of_category = []
        for c in range(len(self.users[username]['expense']['category'])):
            if category == self.users[username]['expense']['category'][c]:
                index_of_category.append(c)
        
        list_by_category = []
        for i in index_of_category:
            list_by_category.append(self.users[username]['expense']['amount'][i])
        
        print(list_by_category)