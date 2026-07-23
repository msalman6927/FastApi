# 04_field_constraints.py
# -----------------------------------------------------------
# GOAL: Add RULES beyond the type:
#   - Field() constraints: gt/ge/lt/le (numbers), min_length/max_length (strings)
#   - @field_validator: custom validation logic you write yourself
#
# This is the declarative version of the @property setters from OOP Day 5.
#
# RUN:  python 04_field_constraints.py
# -----------------------------------------------------------

from pydantic import BaseModel, Field, field_validator, ValidationError


class Account(BaseModel):
    # min_length/max_length constrain string length.
    username: str = Field(min_length=3, max_length=20)
    # gt = greater than, lt = less than (also ge/le for >=, <=).
    age: int = Field(gt=0, lt=150)
    # ge = greater-than-or-equal; default sets the value if omitted.
    balance: float = Field(default=0, ge=0)


# Valid account:
acc = Account(username="ayesha", age=25, balance=1000)
print("Valid account:", acc.model_dump())
print("-" * 50)

# Violating constraints raises ValidationError:
print("username too short:")
try:
    Account(username="ab", age=25)          # min_length=3
except ValidationError as e:
    print(" ", e.errors()[0]["msg"])

print("age out of range:")
try:
    Account(username="ayesha", age=200)     # lt=150
except ValidationError as e:
    print(" ", e.errors()[0]["msg"])

print("negative balance:")
try:
    Account(username="ayesha", age=25, balance=-5)   # ge=0
except ValidationError as e:
    print(" ", e.errors()[0]["msg"])
print("-" * 50)


# ---- Custom rules with @field_validator ----
class SignUp(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_must_have_at(cls, value):
        if "@" not in value or "." not in value:
            raise ValueError("not a valid email address")
        return value.lower()               # RETURN the (cleaned) value - here lowercased

    @field_validator("password")
    @classmethod
    def password_strong(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        if not any(c.isdigit() for c in value):
            raise ValueError("password must contain a digit")
        return value


good = SignUp(email="Ayesha@Mail.COM", password="secret123")
print("Cleaned email (lowercased by validator):", good.email)

print("Weak password:")
try:
    SignUp(email="a@b.com", password="weak")
except ValidationError as e:
    print(" ", e.errors()[0]["msg"])

# REMEMBER: a @field_validator must (1) use @classmethod, (2) raise ValueError
# to reject, and (3) RETURN the value to accept it (forgetting return -> None!).
