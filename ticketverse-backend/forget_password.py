import re
import os
from login import create_account, login
from passlib.hash import pbkdf2_sha256
import random
import string
import smtplib
from email.message import EmailMessage


def generate_reset_token(length=10):
    """Generate a random reset token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_reset_email(email, reset_token):
    """Send password reset email"""
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'your-email@gmail.com'  # Replace with your email
    msg['To'] = email
    msg.set_content(f'Your password reset token is: {reset_token}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your-email@gmail.com', 'your-password')  # Replace with your email and password
        smtp.send_message(msg)


def reset_password(email, reset_token, new_password):
    """Reset password"""
    accounts = load_accounts()
    for account in accounts:
        account_email, _ = account.strip().split(',')
        if email == account_email:
            hashed_password = pbkdf2_sha256.encrypt(new_password)
            with open('accounts.txt', 'w') as file:
                for account in accounts:
                    if account_email != email:
                        file.write(account)
                file.write(f"{email},{hashed_password}\n")
            return True
    return False


def forgot_password():
    """Forgot password"""
    email = input('Enter your email address: ')
    reset_token = generate_reset_token()
    send_reset_email(email, reset_token)
    reset_token_input = input('Enter the reset token sent to your email: ')
    if reset_token_input == reset_token:
        new_password = input('Enter your new password: ')
        if reset_password(email, reset_token, new_password):
            print('Password reset successfully!')
        else:
            print('Account not found.')
    else:
        print('Invalid reset token.')


def load_accounts():
    """Load accounts from file"""
    try:
        with open('accounts.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def main():
    while True:
        print("\n1. Create accounts\n2. Login\n3. Forgot Password\n4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            forgot_password()
        elif choice == '4':
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()