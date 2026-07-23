# solutions.py  (Instructor solution reference for Day 12 assignment)
# -----------------------------------------------------------
# Pydantic v2: BaseModel, Field constraints, @field_validator (+@classmethod),
# nested models, model_dump / model_dump_json / model_validate.
#
# SETUP:  pip install pydantic
# RUN:    python solutions.py
# -----------------------------------------------------------

from pydantic import BaseModel, Field, field_validator, ValidationError


# ===========================================================
# TASK 1 (Easy) — Your first model
# ===========================================================
class Book(BaseModel):
    title: str
    author: str
    pages: int
    in_print: bool = True


print("=== Task 1 ===")
b = Book(title="1984", author="George Orwell", pages=328)
print(f"{b.title} by {b.author}, {b.pages} pages, in print: {b.in_print}")

coerced = Book(title="x", author="y", pages="328")   # string -> int
print("Coerced pages type:", type(coerced.pages).__name__)


# ===========================================================
# TASK 2 (Medium) — Constraints
# ===========================================================
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    category: str = "general"


print("\n=== Task 2 ===")
p = Product(name="Pen", price=50, quantity=100, category="stationery")
print(p.model_dump())

try:
    Product(name="Pen", price=-10, quantity=5)
except ValidationError as e:
    print("Error:", e.errors()[0]["msg"])


# ===========================================================
# TASK 3 (Medium) — Custom validator
# ===========================================================
class Account(BaseModel):
    username: str
    email: str

    @field_validator("username")
    @classmethod
    def no_spaces(cls, value):
        if " " in value:
            raise ValueError("username cannot contain spaces")
        return value.lower()               # return cleaned (lowercased) value

    @field_validator("email")
    @classmethod
    def has_at(cls, value):
        if "@" not in value:
            raise ValueError("email must contain @")
        return value


print("\n=== Task 3 ===")
a = Account(username="Ayesha_K", email="ayesha@mail.com")
print(f"Valid: username={a.username} email={a.email}")

try:
    Account(username="bad name", email="x@y.com")
except ValidationError as e:
    print("Error:", e.errors()[0]["msg"])


# ===========================================================
# TASK 4 (Challenge) — Nested models + serialization
# ===========================================================
class Ingredient(BaseModel):
    name: str
    grams: float = Field(gt=0)


class Recipe(BaseModel):
    title: str
    servings: int = Field(gt=0)
    ingredients: list[Ingredient]
    notes: str | None = None


print("\n=== Task 4 ===")
raw = {
    "title": "Pasta",
    "servings": 2,
    "ingredients": [
        {"name": "Pasta", "grams": 400},
        {"name": "Tomato", "grams": 200},
        {"name": "Cheese", "grams": 50},
    ],
}
recipe = Recipe.model_validate(raw)
print(f"{recipe.title} - {len(recipe.ingredients)} ingredients")
print("Total grams:", sum(i.grams for i in recipe.ingredients))
print(recipe.model_dump_json(indent=2))

bad = {
    "title": "Broken",
    "servings": 1,
    "ingredients": [
        {"name": "A", "grams": 100},
        {"name": "B", "grams": 0},          # invalid: grams must be > 0
    ],
}
try:
    Recipe.model_validate(bad)
except ValidationError as e:
    err = e.errors()[0]
    print(f"Error at {err['loc']}: {err['msg']}")
