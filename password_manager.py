""" ENCRYPT AND SAVE PASSWORD ON TEXT FILE """
from os import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

master_password = input("Type your master password: ")
your_password = input("Type your password: ")

def view():
    """ FUNCTION FOR VIEWING PASSWORDS FROM TEXT FILE """
    with open("passwords.txt", "r", encoding="utf8") as f:
        for i in f.readlines():
            if re.search(rf"{your_password}$", i.rstrip()):
                data = i.rstrip()
                user, passw = data.split("|")
                print(f"{user = }, {passw = }")

def add():
    """ FUNCTION FOR ADDING NAME/PASSWORDS IN TEXT FILE"""
    name = input("Account name: ")
    pwd = input("Password: ")
    pwd = generate_password_hash(pwd, method="scrypt") + your_password
    with open("passwords.txt", "a", encoding="utf8") as f:
        f.write(name + "|" + pwd + "\n")


def add_master():
    """ FUNCTION FOR ADDING MASTER - RUN FIRST AND ONLY ONE TIME PER TEXT FILE """
    print("Password file not found, create master account")
    name = input("Account name: ")
    pwd = input("Password: ")
    pwd = generate_password_hash(pwd, method="scrypt")
    with open("passwords.txt", "a", encoding="utf8") as f:
        f.write(name + "|" + pwd + "\n")


# RUN IF TEXT FILE DOESN'T EXIST
if  os.path.exists("passwords.txt"):

    while True:
        with open("passwords.txt", "r", encoding="utf8") as f:
            master = f.readline().rstrip().split("|")
        if check_password_hash(master[1], master_password):
            mode = input("Would you like to add a new password or view existing ones (view, add, quit)? ").lower()
            if mode == "view":
                view()
            elif mode == "add":
                add()
            elif mode == "quit":
                sys.exit()
            else:
                print("Invalid mode")
                continue
        else:
            print("Incorrect Master Password, exiting")
            sys.exit()

# RUN IF TEXT FILE DOESN'T EXIST
else:
    add_master()
