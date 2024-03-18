import re

def verify_upper_case(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS AN UPPER CASE LETTER

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying if password has upper case letter
    if re.findall("[A-Z]", password):
        return True

    print("You password doesn't have an upper case letter. Try adding at least one.")
    return False

def verify_lower_case(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS LOWER CASE LETTER

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying if password has lower case letter
    if re.findall("[a-z]", password):
        return True

    print("You password doesn't have a lower case letter. Try adding at least one.")
    return False

def verify_number(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS AT LEAST ONE NUMBER

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying if password has a number
    if re.findall("[0-9]", password):
        return True

    print("You password doesn't have a number. Try adding at least one.")
    return False

def verify_special_character(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS AT LEAST ONE SPECIAL CHARACTER

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying if password has special character through verification if there is a character that isn't a letter, number or _

    #for character in password:
      #if special_character == True:
        #break
      #if character.isdigit() == False and character.isupper() == False and character.islower() == False:
        #special_character = True

    if re.findall(r"[^a-zA-Z0-9]", password):
        return True

    print("You password doesn't have a special character. Try adding at least one.")
    return False

def verify_minimum_length(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS AT LEAST 8 CHARACTERS

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying password length
    if len(password) >= 8:
        return True

    print("Your password is too short. It needs at least 8 characters.")
    return False

def verify_common_sequences(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD HAS A COMMON SEQUENCE

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying common sequences
    common_sequences = ["123456", "abcdef"]
    for sequence in common_sequences:
        if sequence in password:
            print("Common sequence found in your password. Try a more complex password.")
            return False
    return True

def verify_common_words(password: str) -> bool:
    """ FUNCTION FOR VERIFYING IF PASSWORD IS IN COMMON WORDS

    Args:
        password (str): password string

    Returns:
        boolean: returns true or false if requirements is met or not
    """

    # Verifying common words
    common_words = ["password", "qwerty"]
    for sequence in common_words:
        if sequence in password:
            print("Common word found in your password. Try a more complex password.")
            return False
    return True

def verify_password_strength() -> str:
    """ FUNCTION FOR VERIFYING IF ALL REQUIREMENTS ARE MET

    Returns:
        str: password string
    """

    # Obtaining password input
    password = input("Password: ").strip()

    # Verifying if all requirements are met
    if verify_common_sequences(password) and verify_common_words(password) and verify_lower_case(password) and verify_upper_case(password) and verify_minimum_length(password) and verify_number(password) and verify_special_character(password):
        print("Your password meets security requirements. Password added.")
        return password

    # Returns error if password doesn't meet requirements
    return "Error"


# if __name__ == "__main__":

    # Obtaining password input
    #password = input().strip()

    # Verifying password strength
    # result = verify_password_strength(password)

    # Printing result
    # print(result)
