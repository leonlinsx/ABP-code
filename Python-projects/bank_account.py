# jetbrains academy project
# create multiple bank account with simple balance options
# uses sqlite database

import sys
import textwrap
import random
import sqlite3

# main bank account class to take user input, create account, login to account
class BankAccount:
    
    IIN = "400000" # Issuer Identification Number (IIN)
    
    # ACCOUNT_PIN_DICT = {}
    
    def __init__(self, database):
        # create the database on program start
        self.database = database
        self.connection = self.database.connect()
        self.database.drop_table(self.connection)
        self.database.create_table(self.connection)
        
    def main(self):
        choice = self.menu_main()
        self.menu_main_choices(choice)
    
    def menu_main(self):
        # prints main menu options and returns user choice
        while True:
            print(textwrap.dedent("""\
                                    1. Create an account
                                    2. Log into account
                                    0. Exit"""))
            menu_choice = int(input().strip())
            # validate input
            if menu_choice not in (1, 2, 0):
                print("Invalid choice, choose again")
                continue
            else:
                break
        return menu_choice
        
    def menu_account(self):
        # prints account menu options and returns user choice
        while True:
            print(textwrap.dedent("""\
                                    1. Balance
                                    2. Add income
                                    3. Do transfer
                                    4. Close account
                                    5. Log out
                                    0. Exit"""))
            menu_choice = int(input().strip())
            if menu_choice not in (1, 2, 3, 4, 5, 0):
                print("Invalid choice, choose again")
                continue
            else:
                break
        return menu_choice
        
    def menu_main_choices(self, choice):
        # takes a choice for main menu and calls appropriate method
        if choice == 1:
            self.account_create()
        elif choice == 2:
            self.account_login()
        elif choice == 0:
            self.menu_main_exit()
        self.main()
    
    def menu_account_choices(self, choice, card_num):
        # takes a choice for account menu and calls appropriate method
        if choice == 1:
            self.account_balance(card_num)
        elif choice == 2:
            self.account_add_income(card_num)
        elif choice == 3:
            self.account_do_transfer(card_num)
        elif choice == 4:
            self.account_close(card_num)
        elif choice == 5:
            self.account_logout()
        elif choice == 0:
            self.menu_main_exit()
        # if not logout or exit, recur the menu_account choices
        new_choice = self.menu_account()
        self.menu_account_choices(new_choice, card_num)
    
    def account_create(self):
        # creates a new, unique card number and pin, prints both
        while True:
            # 16 digit card number of 400000 + 9 digits + 1 checksum
            # the instructions are wrong, the full number is 4000004938320895 and not 400000 + 16 digits + 1 checksum
            # this is wrong -> The seventh digit to the second-to-last digit is the customer account number
            # "customer account number" should have been "account identifier" instead
            acc_id = str(random.randint(10 ** 8, 10 ** 9 - 1))
            checksum = self.checksum(BankAccount.IIN + acc_id)
            card_num = BankAccount.IIN + acc_id + checksum
            # need to take the 0th index of the return sqlite value for all card nums
            all_card_num = [x[0] for x in self.database.get_all_card_num(self.connection)]
            if card_num not in all_card_num:
                break
        # PIN should be generated in a range from 0000 to 9999.
        pin = "{:04}".format(random.randint(0, 9999))
        # BankAccount.ACCOUNT_PIN_DICT.update({card_num: pin})
        self.database.add_card(self.connection, card_num, pin)
        print("\nYour card has been created")
        print("Your card number:")
        print("{}".format(card_num))
        print("Your card PIN:")
        print("{}".format(pin))
        print("")
    
    def account_login(self):
        # takes card number and PIN inputs, validates, and logs in
        print("\nEnter your card number:")
        card_num = input()
        print("Enter your PIN:")
        pin = input()
        valid = self.account_validate(card_num, pin)
        if valid:
            print("\nYou have successfully logged in! \n")
            choice = self.menu_account()
            self.menu_account_choices(choice, card_num)
        else:
            print("\nWrong card number or PIN! \n")
            self.main()
    
    def menu_main_exit(self):
        # prints Bye and exit the main menu
        print("\nBye!")
        sys.exit()
        
    def account_balance(self, card_num):
        # takes an account number, prints balance
        balance = self.database.get_card_balance(self.connection, card_num)[0]
        print("\nBalance: {} \n".format(balance))

    def account_add_income(self, card_num):
        # takes an account number and adds income to it
        print("\nEnter income:")
        try:
            income = int(input())
        except:
            print("Please enter a number!")
        new_bal = self.database.get_card_balance(self.connection, card_num)[0] + income
        self.database.add_balance(self.connection, card_num, new_bal)
        print("Income was added! \n")

    def account_do_transfer(self, card_num):
        # validate transfer choices and do transfer of funds from one card to another
        all_card_num = [x[0] for x in self.database.get_all_card_num(self.connection)]
        balance = self.database.get_card_balance(self.connection, card_num)[0]

        print("\nTransfer")
        print("Enter card number:")
        transfer_num = input()
        # check luhn algo with last digit and first fifteen digits
        actual_luhn = transfer_num[-1]
        pred_luhn = self.checksum(transfer_num[:15])

        if transfer_num == card_num:
            print("You can't transfer money to the same account! \n")
            new_choice = self.menu_account()
            self.menu_account_choices(new_choice, card_num)
        elif actual_luhn != pred_luhn:
            print("Probably you made a mistake in the card number. Please try again! \n")
            new_choice = self.menu_account()
            self.menu_account_choices(new_choice, card_num)
        elif transfer_num not in all_card_num:
            print("Such a card does not exist.\n")
            new_choice = self.menu_account()
            self.menu_account_choices(new_choice, card_num)

        transfer_bal = self.database.get_card_balance(self.connection, transfer_num)[0]
        print("Enter how much money you want to transfer:")
        transfer_amt = int(input())
        if transfer_amt > balance:
            print("Not enough money! \n")
            new_choice = self.menu_account()
            self.menu_account_choices(new_choice, card_num)
        else:
            card_new_bal = balance - transfer_amt
            transfer_new_bal = transfer_bal + transfer_amt
            self.database.add_balance(self.connection, card_num, card_new_bal)
            self.database.add_balance(self.connection, transfer_num, transfer_new_bal)
            print("Success! \n")
            new_choice = self.menu_account()
            self.menu_account_choices(new_choice, card_num)

    def account_close(self, card_num):
        # deletes a card in the database
        self.database.del_card(self.connection, card_num)
        print("\nThe account has been closed! \n")
        self.main()

    def account_logout(self):
        # exits account menu and goes back to main menu
        print("\nYou have successfully logged out! \n")
        self.main()
        
    def account_validate(self, card_num, pin):
        # checks if card number is in the existing database of card numbers
        all_card_num = [x[0] for x in self.database.get_all_card_num(self.connection)]
        if card_num not in all_card_num:
            return False
        # need to take the 0th index of the return sqlite value
        elif pin != self.database.get_card_pin(self.connection, card_num)[0]:
            return False
        else:
            return True
            
    def checksum(self, number):
        # takes a 15 digit number (as str) and returns the 1 digit checksum (as str) according to luhn algo
        # could combine all but I think makes for easier understanding
        first_step = [int(digit) * 2 if (idx + 1) % 2 == 1 else int(digit) for idx, digit in enumerate(number)]
        sec_step = [digit - 9 if digit > 9 else digit for digit in first_step]
        third_step = (10 - (sum(sec_step) % 10)) % 10
        return str(third_step)

# https://www.youtube.com/watch?v=iXYeb2artTE
# creates a db to store the id (pri key), number, pin, balance for accounts
# can also retrieve those info by card number
class Database:

    CREATE_CARD_TABLE = """
    CREATE TABLE IF NOT EXISTS card
    (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)
    """

    DROP_TABLE = "DROP TABLE IF EXISTS card"

    ADD_CARD = "INSERT INTO card (number, pin) VALUES (?, ?)"

    # this is fine, would need diff syntax if unknown col https://stackoverflow.com/a/41411719/13944490
    ADD_BALANCE = "UPDATE card SET balance = ? WHERE number = ?"

    DEL_CARD = "DELETE FROM card WHERE number = ?"

    GET_ALL_CARD_NUM = "SELECT number FROM card"

    GET_CARD_PIN = "SELECT pin FROM card WHERE number = ?"

    GET_CARD_BALANCE = "SELECT balance FROM card WHERE number = ?"

    def __init__(self):
        pass

    def connect(self):
        return sqlite3.connect("card.s3db")

    def create_table(self, connection):
        with connection:
            connection.execute(Database.CREATE_CARD_TABLE)

    def drop_table(self, connection):
        with connection:
            connection.execute(Database.DROP_TABLE)

    def add_card(self, connection, number, pin):
        with connection:
            connection.execute(Database.ADD_CARD, (number, pin))

    def add_balance(self, connection, number, balance):
        with connection:
            connection.execute(Database.ADD_BALANCE, (balance, number))

    def del_card(self, connection, number):
        with connection:
            connection.execute(Database.DEL_CARD, (number,))

    def get_all_card_num(self, connection):
        with connection:
            return connection.execute(Database.GET_ALL_CARD_NUM).fetchall()

    def get_card_pin(self, connection, number):
        with connection:
            return connection.execute(Database.GET_CARD_PIN, (number,)).fetchone()

    def get_card_balance(self, connection, number):
        with connection:
            return connection.execute(Database.GET_CARD_BALANCE, (number,)).fetchone()
        
bank_account = BankAccount(Database())
bank_account.main()