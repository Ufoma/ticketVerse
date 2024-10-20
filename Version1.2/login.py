import re
from accounts import save_account, load_accounts

def get_email():
    """Get and validate email address"""
    while True:
        email = input('Enter email address: ')
        if validate_email(email):
            return email
        print("Invalid email address. Please try again.")


def get_password():
    """Get and validate password"""
    while True:
        password = input('Enter password (min 8 chars, 1 alphabet, 1 number, 1 symbol): ')
        if validate_password(password):
            return password
        print("Password doesn't meet requirements. Please try again.")


def validate_email(email):
    """Validate email address"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_password(password):
    """Validate password"""
    # Define password requirements
    min_length = 8
    has_alphabet = any(char.isalpha() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() for char in password)

    if len(password) < min_length:
        print("Password too short")
    elif not has_alphabet:
        print("Password must contain at least one alphabet")
    elif not has_number:
        print("Password must contain at least one number")
    elif not has_symbol:
        print("Password must contain at least one symbol")
    else:
        return True
    return False


##def create_account():
##    """Create a new account"""
##    print('Create account')
##   email = get_email()
##    password = get_password()
##    print('Your account has been created successfully')
##    return email, password


def create_account():
    print('Create account')
    email = get_email()
    password = get_password()
    save_account(email, password)
    print('Your account has been created successfully')
    return email, password


def login(email, password):
    """Login to existing account"""
    print('Login now!')
    email2 = input('Enter email address: ')
    password2 = input('Enter password: ')

    if email == email2 and password == password2:
        print('Logged in successfully')
    else:
        print('Invalid credentials')


def main():
    email, password = create_account()
    login(email, password)


if __name__ == "__main__":
    main()