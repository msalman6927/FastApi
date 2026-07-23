# 02_crud_with_db.py
# -----------------------------------------------------------
# GOAL: A full CRUD API backed by a REAL database (SQLite via SQLModel).
# Same CRUD shape as Day 17 - only the storage changed. Data now PERSISTS.
#
# SETUP:  pip install sqlmodel "fastapi[standard]"
# RUN:    fastapi dev 02_crud_with_db.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import SQLModel, Field, create_engine, Session, select


# ---- The table model (input/output split shown in the assignment) ----
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    power: str
    age: int | None = None


# ---- Engine + table creation ----
# check_same_thread=False is needed for SQLite with FastAPI's threads.
engine = create_engine("sqlite:///heroes.db",
                       connect_args={"check_same_thread": False})


def get_session():
    """A per-request session (dependency injection - full story Day 19)."""
    with Session(engine) as session:
        yield session


app = FastAPI(title="Heroes DB API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)     # ensure tables exist at boot


# CREATE
@app.post("/heroes", status_code=status.HTTP_201_CREATED)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)        # reload to get the DB-assigned id
    return hero


# READ ALL
@app.get("/heroes")
def list_heroes(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()


# READ ONE
@app.get("/heroes/{hero_id}")
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, detail=f"Hero {hero_id} not found")
    return hero


# UPDATE (partial)
@app.patch("/heroes/{hero_id}")
def update_hero(hero_id: int, changes: dict, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, detail=f"Hero {hero_id} not found")
    for key, value in changes.items():
        setattr(hero, key, value)          # apply provided fields
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


# DELETE
@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, detail=f"Hero {hero_id} not found")
    session.delete(hero)
    session.commit()


# PROVE PERSISTENCE: create a few heroes, STOP the server (Ctrl+C),
# restart with `fastapi dev 02_crud_with_db.py`, and GET /heroes -
# your data is still there. (Compare to Day 17's in-memory loss.)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
