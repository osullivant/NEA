import re
import hashlib

def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)


password1 = input()
print(validate_password(password1))


# adding 5gz as password
salt = "5gz"

# Adding salt at the last of the password
dataBase_password = password1+salt
# Encoding the password
hashed = hashlib.sha256(dataBase_password.encode())

# Printing the Hash
print(hashed.hexdigest())
