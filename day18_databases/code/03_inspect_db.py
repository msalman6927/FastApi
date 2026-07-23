# 03_inspect_db.py
# -----------------------------------------------------------
# GOAL: Prove the data really lives in the database FILE by reading it
# directly - independent of the API. Run this AFTER creating some heroes.
#
# RUN:  python 03_inspect_db.py
# -----------------------------------------------------------

from sqlmodel import SQLModel, Field, create_engine, Session, select


# Must match the table model used elsewhere.
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    power: str
    age: int | None = None


engine = create_engine("sqlite:///heroes.db")


def main():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        if not heroes:
            print("No heroes yet. Create some via the API (02) or the basics script (01).")
            return
        print(f"Found {len(heroes)} heroes stored on disk:")
        for h in heroes:
            print(f"  #{h.id}  {h.name:12} power={h.power}")

    print("\nThese rows were read straight from heroes.db - persistence works.")


if __name__ == "__main__":
    main()
