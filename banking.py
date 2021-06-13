import random
import sqlite3
import os.path


class Card:
    def __init__(self):
        num = "400000" + str(random.randint(100000000, 999999999))
        addition = 0
        for x, y in enumerate([x for x in num]):
            if x % 2 == 0:
                temp = 2 * int(y)
                if temp < 10:
                    addition += temp
                else:
                    addition += (temp - 9)
            else:
                addition += int(y)
        checksum = 0
        if addition % 10 != 0:
            checksum = 10 - addition % 10
        self.card_no = num + str(checksum)
        self.pin = "{0:0>4}".format(str(random.randint(0000, 9999)))
        self.balance = 0
        cur.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)', (self.card_no, self.pin, self.balance))
        conn.commit()


def check_details():
    for row in list(cur.execute('SELECT * FROM card WHERE number=(?)', [card_num])):
        if card_num in row:
            if pin_num in row:
                return True
    return False


def check_card_in_database(card_no):
    for row in list(cur.execute('SELECT * FROM card WHERE number=(?)', [card_no])):
        if card_no in row:
            return True
    return False


def check_luhn(card_no):
    addition = 0
    for x, y in enumerate(card_no):
        if x % 2 == 0:
            temp = 2 * int(y)
            if temp < 10:
                addition += temp
            else:
                addition += (temp - 9)
        else:
            addition += int(y)
    if addition % 10 == 0:
        return True
    return False


def check_balance():
    cur.execute('SELECT balance from card WHERE number=(?)', [card_num])
    balance = cur.fetchone()[0]
    print(f"\nBalance: {balance}")


def add_income():
    print("Enter income:")
    income = int(input())
    cur.execute('UPDATE card SET balance = balance+(?) WHERE number = (?)', (income, card_num))
    conn.commit()
    print("Income was added!")


def do_transfer():
    print("Transfer\nEnter card number:")
    transfer_to = input()
    if check_luhn(transfer_to):
        if check_card_in_database(transfer_to):
            print("How much money you want to transfer:")
            transfer = int(input())
            cur.execute('SELECT balance from card WHERE number=(?)', [card_num])
            balance = cur.fetchone()[0]
            if transfer > balance:
                print("Not enough money!")
            else:
                cur.execute('UPDATE card SET balance=balance-(?) WHERE number=(?)', (transfer, card_num))
                cur.execute('UPDATE card SET balance=balance+(?) WHERE number=(?)', (transfer, transfer_to))
                conn.commit()
                print("Success!")
        else:
            print("Such a card does not exist.")
    else:
        print("Probably you made a mistake in the card number. Please try again!")


def close_account():
    cur.execute('DELETE FROM card WHERE number=(?)', [card_num])
    conn.commit()


if not os.path.exists('card.s3db'):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
    conn.commit()
else:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

flag = 0

while True:
    if flag:
        break
    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = int(input())
    if choice == 0:
        print("Bye!")
        break
    if choice == 1:
        new_user = Card()
        print(f"\nYour card has been created\nYour card number:\n{new_user.card_no}"
              f"\nYour card PIN:\n{new_user.pin}\n")
    if choice == 2:
        print("Enter your card number:")
        card_num = input()
        print("Enter your pin:")
        pin_num = input()

        if check_details():
            print("\nYou have successfully logged in!")
            cur.execute('SELECT * FROM card WHERE number=(?)', [card_num])
            account_details = cur.fetchone()
            while True:
                print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                logged_choice = int(input())
                if logged_choice == 0:
                    flag = 1
                    break
                if logged_choice == 1:
                    check_balance()
                if logged_choice == 2:
                    add_income()
                if logged_choice == 3:
                    do_transfer()
                if logged_choice == 4:
                    close_account()
                if logged_choice == 5:
                    print("You have successfully logged out!")
                    break
        else:
            print("\nWrong card number or PIN!\n")

conn.close()
