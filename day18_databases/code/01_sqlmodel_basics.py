# 01_sqlmodel_basics.py
# -----------------------------------------------------------
# GOAL: Learn the database basics WITHOUT an API first:
# define a table model, create the DB, insert rows, and query them.
#
# SETUP:  pip install sqlmodel
# RUN:    python 01_sqlmodel_basics.py
# (creates a file heroes.db in this folder)
# -----------------------------------------------------------

from sqlmodel import SQLModel, Field, create_engine, Session, select


# A TABLE model = a Pydantic-like model with table=True and a primary key.
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # auto-assigned by DB
    name: str
    power: str
    age: int | None = None


# The ENGINE is the connection to the database file.
# echo=True prints the SQL the ORM generates (great for learning).
engine = create_engine("sqlite:///heroes.db", echo=True)


def main():
    # Create tables from all table=True models (safe to call repeatedly).
    SQLModel.metadata.create_all(engine)

    # A SESSION is a workspace for a batch of operations.
    with Session(engine) as session:
        # CREATE: stage inserts, then commit to save to disk.
        session.add(Hero(name="Deadpond", power="regeneration", age=30))
        session.add(Hero(name="Spider-Boy", power="wall-crawling"))
        session.commit()

    # Query in a fresh session.
    with Session(engine) as session:
        # READ ALL with select()
        heroes = session.exec(select(Hero)).all()
        print("\nAll heroes:")
        for h in heroes:
            print(f"  {h.id}: {h.name} ({h.power}), age={h.age}")

        # READ ONE by primary key
        first = session.get(Hero, 1)
        print("\nHero #1:", first.name)

    print("\nData is now saved in heroes.db - it will still be here next run!")


if __name__ == "__main__":
    main()
