""" ENCRYPT AND SAVE PASSWORD ON TEXT FILE """
from os import sys
from werkzeug.security import generate_password_hash, check_password_hash
import re

master_password = input("Type your master password: ")
your_password = input("Type your password: ")

def view():
    """ FUNCTION FOR VIEWING PASSWORDS FROM TEXT FILE """
    with open("passwords.txt", "r", encoding="utf8") as f:
        if re.search(rf"^[MASTER].*{master_password}", f.readline().rstrip()):
            for i in f.readlines():
                if re.search(rf"{your_password}$", i.rstrip()):
                    data = i.rstrip()
                    user, passw = data.split("|")
                    print(f"{user = }, {passw = }")
        else:
            print("Incorrect Master Password")

def add():
    """ FUNCTION FOR ADDING NAME/PASSWORDS IN TEXT FILE"""
    name = input("Account name: ")
    pwd = input("Password: ")
    pwd = generate_password_hash(pwd, method="scrypt") + master_password
    with open("passwords.txt", "a", encoding="utf8") as f:
        f.write(name + "|" + pwd + "\n")

while True:
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
