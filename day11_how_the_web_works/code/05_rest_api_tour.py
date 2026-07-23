# 05_rest_api_tour.py
# -----------------------------------------------------------
# GOAL: Tie it ALL together with a small REST tour. See how RESOURCES (URLs),
# METHODS (verbs), and STATUS CODES work together on a real REST API.
#
# REST idea: everything is a "resource" at a URL (/users, /users/1),
# and you act on it with HTTP methods. Same URL + different verb = different action.
#
# RUN:  python 05_rest_api_tour.py
# -----------------------------------------------------------

import requests

BASE = "https://jsonplaceholder.typicode.com"


def call(method, path, body=None):
    """Make a request and print a tidy summary line."""
    url = f"{BASE}{path}"
    response = requests.request(method, url, json=body, timeout=10)
    print(f"{method:6} {path:20} -> {response.status_code}")
    return response


print("A tiny REST tour of the /posts and /users resources:\n")

# READ a collection (list of resources)
r = call("GET", "/posts")
print(f"       (got a list of {len(r.json())} posts)\n")

# READ a single resource by id
r = call("GET", "/posts/1")
print(f"       title: {r.json()['title'][:40]}...\n")

# CREATE a new resource (POST with a body) -> expect 201 Created
r = call("POST", "/posts", body={"title": "Hello", "body": "World", "userId": 1})
print(f"       created post id: {r.json()['id']}\n")

# UPDATE a resource (PUT) -> expect 200
r = call("PUT", "/posts/1", body={"id": 1, "title": "Edited", "userId": 1})
print(f"       updated title: {r.json()['title']}\n")

# DELETE a resource -> expect 200
call("DELETE", "/posts/1")
print()

# READ a DIFFERENT resource type - notice the URL is a NOUN (/users)
r = call("GET", "/users/1")
print(f"       user name: {r.json()['name']}\n")

# Ask for something that doesn't exist -> 404
call("GET", "/posts/99999999")

print("\nNotice the pattern:")
print("  - URLs are NOUNS describing resources (/posts, /users/1)")
print("  - HTTP METHODS are the VERBS (GET/POST/PUT/DELETE)")
print("  - STATUS CODES report the outcome (200/201/404)")
print("  - Data flows as JSON")
print("\nThat pattern IS a REST API. Next: on Day 13 we BUILD our own with FastAPI.")
