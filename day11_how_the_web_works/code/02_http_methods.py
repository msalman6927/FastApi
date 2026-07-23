# 02_http_methods.py
# -----------------------------------------------------------
# GOAL: See the main HTTP METHODS (verbs) in action and how they map to
# CRUD (Create, Read, Update, Delete).
#
#   GET    -> Read    (fetch data,   no body)
#   POST   -> Create  (new resource, has body)
#   PUT    -> Update  (replace,      has body)
#   DELETE -> Delete  (remove,       no body)
#
# RUN:  python 02_http_methods.py
# -----------------------------------------------------------

import requests

BASE = "https://jsonplaceholder.typicode.com"    # a fake REST API for practice

# ---- GET (Read): fetch an existing resource ----
print("GET /posts/1  (Read)")
r = requests.get(f"{BASE}/posts/1", timeout=10)
print("  status:", r.status_code, "| title:", r.json()["title"][:30], "...")
print("-" * 55)

# ---- POST (Create): send a body to create a new resource ----
# We send data in the request BODY as JSON using the json= argument.
print("POST /posts  (Create)")
new_post = {"title": "My First API Post", "body": "Hello world", "userId": 99}
r = requests.post(f"{BASE}/posts", json=new_post, timeout=10)
print("  status:", r.status_code, "(201 = Created)")
print("  server returned new resource with id:", r.json()["id"])
print("-" * 55)

# ---- PUT (Update): replace an existing resource ----
print("PUT /posts/1  (Update/replace)")
updated = {"id": 1, "title": "Updated title", "body": "New body", "userId": 1}
r = requests.put(f"{BASE}/posts/1", json=updated, timeout=10)
print("  status:", r.status_code, "| new title:", r.json()["title"])
print("-" * 55)

# ---- DELETE (Delete): remove a resource ----
print("DELETE /posts/1  (Delete)")
r = requests.delete(f"{BASE}/posts/1", timeout=10)
print("  status:", r.status_code, "(200 = deleted OK)")
print("-" * 55)

# NOTE: jsonplaceholder is a FAKE API - it pretends to create/update/delete
# and returns realistic responses, but doesn't really change anything.
# Perfect for learning the METHODS safely.
print("Same URL + different METHOD = different action. That's REST.")
