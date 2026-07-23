# 04_working_with_json.py
# -----------------------------------------------------------
# GOAL: JSON is the language of APIs. Learn to convert between JSON text
# and Python objects.
#
#   json.dumps(obj)  -> Python  TO  JSON string   ("dump String")
#   json.loads(text) -> JSON string  TO  Python    ("load String")
#   response.json()  -> parse an API response body into Python (requests)
#
# RUN:  python 04_working_with_json.py
# -----------------------------------------------------------

import json
import requests

# ---- A Python dictionary ----
person = {
    "id": 5,
    "name": "Ayesha",
    "is_active": True,        # Python True ...
    "roles": ["admin", "editor"],
    "profile": {"age": 25, "city": "Karachi"},
    "nickname": None,         # Python None ...
}

# ---- Python -> JSON string (json.dumps) ----
json_text = json.dumps(person, indent=2)
print("Python dict converted to JSON text:\n")
print(json_text)
# Notice in the JSON: True -> true, None -> null, and ALL keys use "double quotes".
print("-" * 50)

# ---- JSON string -> Python (json.loads) ----
back_to_python = json.loads(json_text)
print("JSON text parsed back to Python:")
print("  type:", type(back_to_python))          # dict
print("  name:", back_to_python["name"])        # Ayesha
print("  first role:", back_to_python["roles"][0])
print("-" * 50)

# ---- JSON <-> Python type mapping (the whole trick) ----
print("JSON  ->  Python")
print("{}    ->  dict")
print("[]    ->  list")
print('"..." ->  str')
print("num   ->  int/float")
print("true  ->  True   |  false -> False")
print("null  ->  None")
print("-" * 50)

# ---- In practice: requests parses JSON responses for you ----
r = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
user = r.json()                                  # JSON body -> Python dict
print("Fetched user (via response.json()):")
print("  name:", user["name"])
print("  email:", user["email"])
print("  city:", user["address"]["city"])        # nested objects -> nested dicts
