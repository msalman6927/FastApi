# solutions.py  (Day 16 - response_model, status codes, HTTPException)
# SETUP: pip install "fastapi[standard]"
# RUN:   fastapi dev solutions.py  ->  /docs

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Day 16 Solutions")


# ===== Task 1 - hide a field =====
class AccountIn(BaseModel):
    username: str
    email: str
    password: str

class AccountOut(BaseModel):
    username: str
    email: str

ACCOUNTS: list[AccountIn] = []

@app.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(acc: AccountIn):
    ACCOUNTS.append(acc)
    return acc                      # password stripped by response_model


# ===== Tasks 2-4 combined into a Book API =====
class BookIn(BaseModel):
    title: str
    author: str
    secret_notes: str = ""          # internal - must not be exposed

class BookOut(BaseModel):
    id: int
    title: str
    author: str

BOOKS: dict[int, BookIn] = {}
_next = 1


@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn):
    global _next
    # 409 if a book with the same title already exists
    if any(b.title == book.title for b in BOOKS.values()):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail=f"Book '{book.title}' already exists")
    book_id = _next
    BOOKS[book_id] = book
    _next += 1
    return {"id": book_id, "title": book.title, "author": book.author}


@app.get("/books", response_model=list[BookOut])
def list_books():
    return [{"id": i, "title": b.title, "author": b.author}
            for i, b in BOOKS.items()]


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    b = BOOKS.get(book_id)
    if b is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Book {book_id} not found")
    return {"id": book_id, "title": b.title, "author": b.author}


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookIn):
    if book_id not in BOOKS:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Book {book_id} not found")
    BOOKS[book_id] = book
    return {"id": book_id, "title": book.title, "author": book.author}


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id not in BOOKS:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Book {book_id} not found")
    del BOOKS[book_id]
    # 204 -> no body


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
