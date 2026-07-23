# solutions.py  (Instructor solution reference for Day 15 assignment)
# -----------------------------------------------------------
# Request bodies with Pydantic models: POST/PUT, validation -> 422,
# in-memory storage, body+path+query, and nested bodies.
#
# SETUP:  pip install "fastapi[standard]"
# RUN:    fastapi dev solutions.py  ->  http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Day 15 Solutions")


# ===========================================================
# TASK 1 — First POST
# ===========================================================
class Student(BaseModel):
    name: str
    age: int
    email: str


@app.post("/students")
def create_student(student: Student):
    return {"message": f"created {student.name}", "student": student}


# ===========================================================
# TASK 2 — Validation + store + list
# ===========================================================
class Product(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
    in_stock: bool = True


PRODUCTS: list[Product] = []


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    PRODUCTS.append(product)          # only reached if validation passed
    return product


@app.get("/products")
def list_products():
    return PRODUCTS


# ===========================================================
# TASK 3 — Body + path + query, and PUT
# ===========================================================
class Task(BaseModel):
    title: str
    done: bool = False


TASKS: dict[int, Task] = {
    1: Task(title="Learn POST", done=False),
    2: Task(title="Learn PUT", done=False),
}


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_id = max(TASKS.keys(), default=0) + 1
    TASKS[new_id] = task
    return {"id": new_id, "task": task}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, notify: bool = False):
    TASKS[task_id] = task             # replace (404 handling comes Day 16)
    return {"id": task_id, "updated": task, "notify": notify}


# ===========================================================
# TASK 4 — Nested body: a shopping cart
# ===========================================================
class CartItem(BaseModel):
    product: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class Cart(BaseModel):
    customer: str
    items: list[CartItem]             # list of nested models


@app.post("/carts")
def create_cart(cart: Cart):
    total_qty = sum(i.quantity for i in cart.items)
    total_price = sum(i.quantity * i.price for i in cart.items)
    return {
        "customer": cart.customer,
        "item_count": len(cart.items),
        "total_quantity": total_qty,
        "total_price": total_price,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
