# solutions.py  (Day 18 - SQLModel + SQLite, full CRUD, input/output models)
# SETUP: pip install sqlmodel "fastapi[standard]"
# RUN:   fastapi dev solutions.py  ->  /docs

from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import SQLModel, Field, create_engine, Session, select


# ---- Table model (Task 1) ----
class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int


# ---- API models (Task 3) ----
class BookCreate(SQLModel):
    title: str
    author: str
    year: int

class BookPublic(SQLModel):
    id: int
    title: str
    author: str
    year: int

class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


engine = create_engine("sqlite:///books.db",
                       connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(title="Books DB API")


@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)


@app.post("/books", response_model=BookPublic, status_code=201)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# Task 4: filtering via query params
@app.get("/books", response_model=list[BookPublic])
def list_books(author: str | None = None, min_year: int | None = None,
               session: Session = Depends(get_session)):
    query = select(Book)
    if author:
        query = query.where(Book.author == author)
    if min_year is not None:
        query = query.where(Book.year >= min_year)
    return session.exec(query).all()


@app.get("/books/{book_id}", response_model=BookPublic)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(404, detail=f"Book {book_id} not found")
    return book


@app.patch("/books/{book_id}", response_model=BookPublic)
def update_book(book_id: int, changes: BookUpdate,
                session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(404, detail=f"Book {book_id} not found")
    for key, value in changes.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(404, detail=f"Book {book_id} not found")
    session.delete(book)
    session.commit()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
