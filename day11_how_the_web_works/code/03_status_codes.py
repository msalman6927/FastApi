# 03_status_codes.py
# -----------------------------------------------------------
# GOAL: Understand STATUS CODES - the 3-digit number the server returns
# to say how the request went.
#
#   2xx = Success        ("it worked")
#   3xx = Redirection    ("look elsewhere")
#   4xx = Client error   ("YOU messed up" - bad request, not found)
#   5xx = Server error   ("the SERVER messed up")
#
# RUN:  python 03_status_codes.py
# -----------------------------------------------------------

import requests

BASE = "https://jsonplaceholder.typicode.com"


def family(code):
    """Return the human name of a status-code family from its first digit."""
    return {
        2: "Success",
        3: "Redirection",
        4: "Client error (your fault)",
        5: "Server error (server's fault)",
    }.get(code // 100, "Informational/Unknown")


def show(label, url):
    r = requests.get(url, timeout=10)
    print(f"{label}")
    print(f"  URL: {url}")
    print(f"  -> {r.status_code}  [{family(r.status_code)}]")
    print()


# 200 OK: the resource exists and is returned.
show("Existing resource:", f"{BASE}/posts/1")

# 404 Not Found: asking for something that doesn't exist.
show("Missing resource:", f"{BASE}/posts/99999999")

# httpbin.org can return ANY status code we ask for - great for practice.
show("Force a 200:", "https://httpbin.org/status/200")
show("Force a 404:", "https://httpbin.org/status/404")
show("Force a 500:", "https://httpbin.org/status/500")
show("Force a 201:", "https://httpbin.org/status/201")

print("Remember: 2=good, 4=YOU messed up, 5=SERVER messed up.")
print("Key ones: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized,")
print("          404 Not Found, 422 Validation error, 500 Server error.")
