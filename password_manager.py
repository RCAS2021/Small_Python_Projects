""" ENCRYPT AND SAVE PASSWORD ON TEXT FILE """
from os import sys
master_password = input("Type your master password: ")

def view():
    pass

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a", encoding="utf8") as f:
        f.write(name + "|" + pwd)

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add)? ").lower()
    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode")
        continue

    stop = input("Quit? Y/N ").lower()
    if stop != "n":
        sys.exit()
