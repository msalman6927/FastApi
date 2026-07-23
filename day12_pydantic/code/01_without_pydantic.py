# 01_without_pydantic.py
# -----------------------------------------------------------
# GOAL: Feel the PAIN of validating data BY HAND. Then Pydantic will
# replace all of this with a few lines.
#
# RUN:  python 01_without_pydantic.py
# -----------------------------------------------------------

# Imagine this arrived as a parsed JSON body from an API request.
# We CANNOT trust it - fields may be missing or the wrong type.
incoming = {"name": "Ayesha", "age": "twenty", "email": "not-an-email"}


def validate_user(data):
    """Hand-written validation. Tedious, repetitive, easy to get wrong."""
    # Check 'name' exists and is a string
    if "name" not in data:
        raise ValueError("name is required")
    if not isinstance(data["name"], str):
        raise ValueError("name must be a string")

    # Check 'age' exists and is an int
    if "age" not in data:
        raise ValueError("age is required")
    if not isinstance(data["age"], int):
        raise ValueError("age must be an integer")

    # Check 'email' looks like an email (very rough)
    if "email" not in data or "@" not in data["email"]:
        raise ValueError("email is invalid")

    return data


try:
    validate_user(incoming)
except ValueError as e:
    print("Validation failed:", e)

# Problems with this approach:
#   - We repeat these checks for EVERY field and EVERY endpoint.
#   - We must remember every type, every rule, by hand.
#   - No automatic type conversion ("25" stays a string).
#   - Error messages are inconsistent.
#
# WISH: declare the shape ONCE and get validation + conversion + clear
# errors for free. --> That is PYDANTIC. See file 02.
print("\nThere must be a better way... enter Pydantic (file 02).")
