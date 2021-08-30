import re

def full_name_validator(full_name):
    """The full_name must contain just letters.

    Args:
        full_name (Charfield): Replace the empty spaces between
        the words to math with isalpha method.

    Returns:
        boolean: True if all the characters are alphabet letters
    """
    full_name = full_name.replace(" ", "")
    return full_name.isalpha()

def password_validator(password):
    """The password must contain at least one number
    and one uppercase and lowercase letter, and at least
    8 or more characters.

    Args:
        password (Charfield): The user's password

    Returns:
        regex: the result of the regex expression
    """
    pattern = '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}'
    validation = re.fullmatch(pattern, password)
    return validation