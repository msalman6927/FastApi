# Day 12 Assignment — Pydantic

**Module 02 · Day 12**
**Goal:** Define Pydantic models with types, constraints, custom validators, and nested structures — and serialize them to/from JSON.

> Reminder: activate your `.venv`. `pip install pydantic`. We use **Pydantic v2** — use `@field_validator` (+ `@classmethod`), `model_dump()`, `model_dump_json()`, `model_validate()`. If a tutorial uses `.dict()` or `@validator`, it's the old v1.

---

## Task 1 (Easy) — Your first model
1. Create a model `Book` with fields: `title: str`, `author: str`, `pages: int`, and `in_print: bool = True`.
2. Create a valid book and print each field.
3. Create a book passing `pages` as the **string** `"328"` and show that Pydantic coerces it to an `int`.

**Expected output (example):**
```
1984 by George Orwell, 328 pages, in print: True
Coerced pages type: int
```

---

## Task 2 (Medium) — Constraints
1. Create a model `Product` with:
   - `name: str` — length between 2 and 50,
   - `price: float` — greater than 0,
   - `quantity: int` — greater than or equal to 0,
   - `category: str = "general"` (optional, default).
2. Create a valid product and print it via `model_dump()`.
3. In a try/except, attempt to create a product with `price = -10` and print the validation error message.

**Expected output (example):**
```
{'name': 'Pen', 'price': 50.0, 'quantity': 100, 'category': 'stationery'}
Error: Input should be greater than 0
```

---

## Task 3 (Medium) — Custom validator
1. Create a model `Account` with `username: str` and `email: str`.
2. Add a `@field_validator` on `username` that rejects usernames containing spaces and returns the username **lowercased**.
3. Add a `@field_validator` on `email` that rejects a value without `@`.
4. Show a valid account (verify the username came out lowercased), and a rejected one (username with a space).

**Expected output (example):**
```
Valid: username=ayesha_k email=ayesha@mail.com
Error: username cannot contain spaces
```

---

## Task 4 (Challenge) — Nested models + serialization
1. Create these models:
   - `Ingredient`: `name: str`, `grams: float = Field(gt=0)`.
   - `Recipe`: `title: str`, `servings: int = Field(gt=0)`, `ingredients: list[Ingredient]`, `notes: str | None = None`.
2. Build a `Recipe` from a nested dict (use `model_validate`) with at least 3 ingredients.
3. Print:
   - the recipe title and number of ingredients,
   - the total grams of all ingredients,
   - the recipe as a JSON string (`model_dump_json(indent=2)`).
4. In a try/except, validate a recipe where one ingredient has `grams: 0` and print the error path (`err['loc']`) and message.

**Expected output (example):**
```
Pasta - 3 ingredients
Total grams: 650.0
{ ...pretty JSON... }
Error at ('ingredients', 1, 'grams'): Input should be greater than 0
```

---

## Submission
Put all four tasks in `day12_solution.py`, commit to repo `batch5-day12`, push to GitHub, and submit the link.

## Grading checklist
- [ ] Task 1 model works; string `"328"` coerced to int
- [ ] Task 2 constraints enforced; `price=-10` rejected
- [ ] Task 3 custom validators lowercase username and reject invalid input
- [ ] Task 4 uses nested models + a list of models
- [ ] Task 4 serializes with `model_dump_json` and reads a nested error path
- [ ] Uses Pydantic v2 syntax throughout
