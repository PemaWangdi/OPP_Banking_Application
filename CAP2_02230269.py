#02230269
#reference https://www.youtube.com/watch?v=julcNz6rWVc&t=25s
#reference https://www.youtube.com/watch?v=xTh-ln2XhgU
#reference https://www.youtube.com/watch?v=BRssQPHZMrc

import random  # Importing the random module for generating random account numbers and passwords
import os  # Importing the os module for file operations

# Define the base class for any type of account
class BankAccount:
    def __init__(self, account_number, password, account_type, balance=0.0):
        # Initialize account with number, password, type, and balance
        self.acc_number = account_number
        self.passwd = password
        self.acc_type = account_type
        self.balance = balance

    def deposit(self, amount):
        # Method to deposit amount into the account
        self.balance += amount  
        print(f"Deposited {amount}. New balance: {self.balance}")  

    def withdraw(self, amount):
        # Method to withdraw amount from the account
        if self.balance >= amount:  
            self.balance -= amount  
            print(f"Withdrew {amount}. New balance: {self.balance}")  
        else:
            print("Insufficient funds.")  

    def __str__(self):
        # String representation of the account object
        return f"Account Number: {self.acc_number}, Balance: {self.balance}, Type: {self.acc_type}"

# Define subclass for personal accounts
class PersonalAccount(BankAccount):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize personal account using the parent class constructor
        super().__init__(account_number, password, "Personal", balance)

# Define subclass for business accounts
class BusinessAccount(BankAccount):
    def __init__(self, account_number, password, balance=0.0):
        # Initialize business account using the parent class constructor
        super().__init__(account_number, password, "Business", balance)

# Define the class to manage all bank operations
class BankingSystem:
    def __init__(self, accounts_file="accounts.txt"):
        # Initialize bank with accounts file
        self.accounts_file = accounts_file  
        self.load_accounts()  

    def load_accounts(self):
        # Method to load accounts from file
        self.accounts = {}  
        if os.path.exists(self.accounts_file):  
            with open(self.accounts_file, "r") as file:  
                for line in file:  
                    acc_num, passwd, acc_type, balance = line.strip().split(",")  
                    balance = float(balance)  
                    if acc_type == "Personal":  
                        account = PersonalAccount(acc_num, passwd, balance)  
                    elif acc_type == "Business":  
                        account = BusinessAccount(acc_num, passwd, balance)  
                    self.accounts[acc_num] = account  

    def save_accounts(self):
        # Method to save accounts to file
        with open(self.accounts_file, "w") as file:  
            for account in self.accounts.values():  
                file.write(f"{account.acc_number},{account.passwd},{account.acc_type},{account.balance}\n")  

    def create_account(self, acc_type):
        # Method to create a new account
        acc_number = str(random.randint(10000, 99999))  
        password = str(random.randint(1000, 9999))  
        if acc_type == "Personal":  
            account = PersonalAccount(acc_number, password)  
        elif acc_type == "Business":  
            account = BusinessAccount(acc_number, password)  
        self.accounts[acc_number] = account  
        self.save_accounts()  
        print(f"Account created successfully. Account Number: {acc_number}, Password: {password}")  

    def login(self, acc_number, password):
        # Method to login to an account
        account = self.accounts.get(acc_number)  
        if account and account.passwd == password:  
            return account  
        else:
            print("Invalid account number or password.")  
            return None  

    def delete_account(self, acc_number):
        # Method to delete an account
        if acc_number in self.accounts:  
            del self.accounts[acc_number]  
            self.save_accounts()  
            print(f"Account {acc_number} deleted successfully.")  
        else:
            print("Account does not exist.")  

    def transfer_money(self, from_account, to_account_number, amount):
        # Method to transfer money between accounts
        if from_account.balance < amount:  
            print("Insufficient funds.")  
            return  
        to_account = self.accounts.get(to_account_number)  
        if to_account:  
            from_account.withdraw(amount)  
            to_account.deposit(amount)  
            self.save_accounts()  
            print(f"Transferred {amount} from {from_account.acc_number} to {to_account_number}.")  
        else:
            print("Receiving account does not exist.")  

def main():
    bank_system = BankingSystem()  
    while True:
        # Display main menu
        print("\nWelcome to the Banking Application")
        print("1. Open an Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")  

        if choice == '1':
            # Option to open a new account
            acc_type = input("Enter account type (Personal/Business): ")  
            bank_system.create_account(acc_type)  

        elif choice == '2':
            # Option to login to an account
            acc_number = input("Enter your account number: ")  
            password = input("Enter your password: ")  
            account = bank_system.login(acc_number, password)  
            if account:
                while True:
                    # Display account menu
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Fund Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    user_choice = input("Choose an option: ")  

                    if user_choice == '1':
                        # Option to check balance
                        print(f"Balance: {account.balance}")  

                    elif user_choice == '2':
                        # Option to deposit money
                        amount = float(input("Enter amount to deposit: "))  
                        account.deposit(amount)  
                        bank_system.save_accounts()  

                    elif user_choice == '3':
                        # Option to withdraw money
                        amount = float(input("Enter amount to withdraw: "))  
                        account.withdraw(amount)  
                        bank_system.save_accounts()  

                    elif user_choice == '4':
                        # Option to transfer money
                        to_account_number = input("Enter the recipient account number: ")  
                        amount = float(input("Enter amount to transfer: "))  
                        bank_system.transfer_money(account, to_account_number, amount)  

                    elif user_choice == '5':
                        # Option to delete account
                        bank_system.delete_account(account.acc_number)  
                        break  

                    elif user_choice == '6':
                        # Option to logout
                        break  

                    else:
                        print("Invalid choice. Please try again.")  

        elif choice == '3':
            # Option to exit the application
            print("Thank you for using the Banking Application. Goodbye!")  
            break  

        else:
            print("Invalid choice. Please try again.")  

if __name__ == "__main__":
    main()  
