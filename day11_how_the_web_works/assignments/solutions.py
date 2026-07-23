# solutions.py  (Instructor solution reference for Day 11 assignment)
# -----------------------------------------------------------
# Concepts: HTTP requests/responses, methods, status codes, JSON, REST,
# using the `requests` library.
#
# SETUP:  pip install requests
# RUN:    python solutions.py
# -----------------------------------------------------------

# ===========================================================
# PART A (Written) — Concept check
# ===========================================================
# 1. Client = you/the customer (browser, script, agent); Waiter = HTTP (carries
#    the messages); Kitchen = the server (does the work, returns the data).
# 2. Method (verb), URL (address), Headers (metadata), Body (data sent).
# 3. 2xx = success ("it worked"); 4xx = client error ("you sent something wrong");
#    5xx = server error ("the server failed").
# 4. json.dumps() = Python object -> JSON string (dump to String);
#    json.loads() = JSON string -> Python object (load from String).
# 5. Because the HTTP method already IS the verb (GET/POST/...). The URL should
#    name the resource (a noun); the verb comes from the method. Cleaner + RESTful.

import requests

BASE = "https://jsonplaceholder.typicode.com"


# ===========================================================
# TASK 1 (Easy) — Your first request
# ===========================================================
print("=== Task 1 ===")
r = requests.get(f"{BASE}/todos/1", timeout=10)
print("Status:", r.status_code)
data = r.json()
print("Title:", data["title"])
print("Completed:", data["completed"])


# ===========================================================
# TASK 2 (Medium) — Explore status codes
# ===========================================================
print("\n=== Task 2 ===")

def check(url):
    r = requests.get(url, timeout=10)
    fam = {
        2: "Success",
        3: "Redirection",
        4: "Client error (your fault)",
        5: "Server error (server's fault)",
    }.get(r.status_code // 100, "Unknown")
    print(f"{r.status_code} -> {fam}")

check(f"{BASE}/posts/1")
check(f"{BASE}/posts/99999999")
check("https://httpbin.org/status/500")


# ===========================================================
# TASK 3 (Medium) — Create a resource (POST) and read nested JSON
# ===========================================================
print("\n=== Task 3 ===")
new_post = {"title": "Learning APIs", "body": "Day 11", "userId": 1}
r = requests.post(f"{BASE}/posts", json=new_post, timeout=10)
print(f"Created post, status {r.status_code}, id {r.json()['id']}")

r = requests.get(f"{BASE}/users/2", timeout=10)
u = r.json()
print(f"User 2: {u['name']} | {u['email']} | {u['company']['name']}")


# ===========================================================
# TASK 4 (Challenge) — Build a tiny API client
# ===========================================================
print("\n=== Task 4 ===")

def get_user_todos(user_id):
    # The query string ?userId=<id> asks the server to FILTER the list.
    url = f"{BASE}/todos?userId={user_id}"
    r = requests.get(url, timeout=10)
    return r.json()          # a list of todo dicts


try:
    todos = get_user_todos(1)
    total = len(todos)
    completed = sum(1 for t in todos if t["completed"])
    not_done = total - completed
    print(f"User 1 has {total} todos")
    print(f"Completed: {completed} | Not completed: {not_done}")

    # First incomplete todo's title:
    first_incomplete = next(t for t in todos if not t["completed"])
    print("First incomplete:", first_incomplete["title"])
except requests.exceptions.RequestException:
    print("No internet connection - could not reach the API.")
