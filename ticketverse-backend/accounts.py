import os
from passlib.hash import pbkdf2_sha256


def save_account(email, password):
    hashed_password = pbkdf2_sha256.encrypt(password)
    with open('accounts.txt', 'a') as file:
        file.write(f"{email},{hashed_password}\n")


def load_accounts():
    try:
        with open('accounts.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []