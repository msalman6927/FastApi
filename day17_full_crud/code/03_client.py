# 03_client.py
# -----------------------------------------------------------
# GOAL: Exercise the CRUD API from Python (a real client), proving every
# operation works end to end.
#
# HOW TO USE:
#   Terminal 1:  fastapi dev 01_crud_items.py     (start the server)
#   Terminal 2:  python 03_client.py              (run this client)
# -----------------------------------------------------------

import requests

BASE = "http://127.0.0.1:8000"


def main():
    # CREATE two items
    r = requests.post(f"{BASE}/items", json={"name": "Pen", "price": 50})
    print("CREATE:", r.status_code, r.json())          # 201
    pen_id = r.json()["id"]

    requests.post(f"{BASE}/items", json={"name": "Book", "price": 300})

    # READ ALL
    print("LIST:", requests.get(f"{BASE}/items").json())

    # READ ONE
    print("GET one:", requests.get(f"{BASE}/items/{pen_id}").json())

    # READ missing -> 404
    r = requests.get(f"{BASE}/items/999")
    print("GET missing:", r.status_code, r.json())      # 404

    # UPDATE
    r = requests.put(f"{BASE}/items/{pen_id}", json={"name": "Blue Pen", "price": 60})
    print("UPDATE:", r.status_code, r.json())           # 200

    # DELETE
    r = requests.delete(f"{BASE}/items/{pen_id}")
    print("DELETE:", r.status_code)                     # 204

    # Confirm it's gone
    print("After delete, LIST:", requests.get(f"{BASE}/items").json())


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Could not connect. Start the server first:")
        print("  fastapi dev 01_crud_items.py")
