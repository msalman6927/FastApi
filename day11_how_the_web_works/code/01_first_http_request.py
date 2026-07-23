# 01_first_http_request.py
# -----------------------------------------------------------
# GOAL: Make a REAL HTTP request from Python and inspect the response.
# This is the "aha" moment: your code talks to a server across the world.
#
# SETUP:  pip install requests      (already installed on Day 1)
# RUN:    python 01_first_http_request.py
# -----------------------------------------------------------

import requests

# We'll ask a free public test API for one "post" (like a blog post).
# The URL identifies WHAT we want and WHERE it lives.
url = "https://jsonplaceholder.typicode.com/posts/1"

print(f"Sending a GET request to:\n  {url}\n")

# requests.get(url) sends an HTTP GET request and waits for the response.
response = requests.get(url, timeout=10)

# ---- Part 1 of a response: the STATUS CODE (did it work?) ----
print("STATUS CODE:", response.status_code)      # 200 = OK (success)
print("Was it successful?", response.ok)          # True for 2xx codes

# ---- Part 2 of a response: HEADERS (metadata about the response) ----
# Headers describe the response, e.g. what format the body is in.
print("Content-Type header:", response.headers.get("Content-Type"))

# ---- Part 3 of a response: the BODY (the actual data) ----
# As raw text:
print("\nRAW BODY (text):")
print(response.text)

# The body here is JSON. .json() parses it into a Python dictionary for us.
data = response.json()
print("\nPARSED BODY (Python dict):")
print("  type:", type(data))
print("  title:", data["title"])
print("  userId:", data["userId"])

print("\nYou just had a request -> response conversation with a real server!")
