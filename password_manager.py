""" ENCRYPT AND SAVE PASSWORD ON TEXT FILE """
from os import sys
master_password = input("Type your master password: ")

def view():
    """ FUNCTION FOR VIEWING PASSWORDS FROM TEXT FILES """
    with open("passwords.txt", "r", encoding="utf8") as f:
        for i in f.readlines():
            print(i)

def add():
    """ FUNCTION FOR ADDING NAME/PASSWORDS IN TEXT FILE"""
    name = input("Account name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a", encoding="utf8") as f:
        f.write(name + "|" + pwd + "\n")

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
