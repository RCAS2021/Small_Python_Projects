import re

def verify_password_strength(password):

    minimum_length = 8
    upper_case = False
    lower_case = False
    number = False
    special_character = False

    # Verifying common sequences
    common_sequences = ["123456", "abcdef"]
    for sequence in common_sequences:
        if sequence in password:
            return "Your password has common sequences. Try a more complex password."

    # Verifying common words
    common_words = ["password", "qwerty"]
    if password in common_words:
        return "Your password has common words. Try a more complex password."

    # Verifying password length
    if len(password) < minimum_length:
        return f"Your password is too short. Try at least {minimum_length} characters."

    # Verifying if password has lower case letter
    if re.findall("[a-z]", password):
        lower_case = True

    # Verifying if password has upper case letter
    if re.findall("[A-Z]", password):
        upper_case = True

    # Verifying if password has special character through verification if there is a character that isn't a letter, number or _
    if re.findall(r"[^a-zA-Z0-9]", password):
        special_character = True

    #for character in password:
      #if special_character == True:
        #break
      #if character.isdigit() == False and character.isupper() == False and character.islower() == False:
        #special_character = True

    # Verifying if password has a number
    if re.findall("[0-9]", password):
        number = True

    # Verifying if all requirements are met
    if upper_case and lower_case and special_character and number:
        return "Your password meets security requirements."

    # Returns error message if password doesn't meet requirements
    return "Your password doesn't meet security requirements."


# Obtaining password input
password = input().strip()

# Verifying password strength
result = verify_password_strength(password)

# Printing result
print(result)
