# Day 11 Assignment — How the Web Works

**Module 02 · Day 11**
**Goal:** Prove you understand HTTP requests/responses, methods, status codes, JSON, and REST by actually calling public APIs from Python.

> Reminder: activate your `.venv`. `pip install requests` if needed. All tasks use free, no-auth public APIs (`jsonplaceholder.typicode.com`, `httpbin.org`). Internet required.

There is a short **written part** and a **coding part**. Put written answers as comments at the top of your solution file.

---

## Part A (Written) — Concept check
Answer these in comments (1–2 lines each):
1. In the restaurant analogy, what are the client, the waiter, and the kitchen?
2. Name the four parts of an HTTP request.
3. What does each status-code family mean: 2xx, 4xx, 5xx?
4. What's the difference between `json.dumps()` and `json.loads()`?
5. Why do REST URLs use nouns (`/users/5`) instead of verbs (`/getUser?id=5`)?

---

## Task 1 (Easy) — Your first request
1. Use `requests` to GET `https://jsonplaceholder.typicode.com/todos/1`.
2. Print the **status code**.
3. Parse the JSON and print the `title` and whether it's `completed`.

**Expected output (example):**
```
Status: 200
Title: delectus aut autem
Completed: False
```

---

## Task 2 (Medium) — Explore status codes
1. Write a function `check(url)` that GETs the URL and prints the status code **and** its family name ("Success", "Client error", "Server error", etc.).
2. Call it on:
   - `https://jsonplaceholder.typicode.com/posts/1` (should be 200)
   - `https://jsonplaceholder.typicode.com/posts/99999999` (should be 404)
   - `https://httpbin.org/status/500` (forced 500)

**Expected output (example):**
```
200 -> Success
404 -> Client error (your fault)
500 -> Server error (server's fault)
```

---

## Task 3 (Medium) — Create a resource (POST) and read JSON
1. POST a new "post" to `https://jsonplaceholder.typicode.com/posts` with a JSON body containing `title`, `body`, and `userId` (your choice).
2. Print the returned **status code** (should be 201) and the **id** the server assigned.
3. Then GET `https://jsonplaceholder.typicode.com/users/2` and print that user's `name`, `email`, and `company` name (hint: it's nested — `data["company"]["name"]`).

**Expected output (example):**
```
Created post, status 201, id 101
User 2: Ervin Howell | Shanna@melissa.tv | Deckow-Crist
```

---

## Task 4 (Challenge) — Build a tiny API client
1. Write a function `get_user_todos(user_id)` that:
   - GETs `https://jsonplaceholder.typicode.com/todos?userId=<user_id>` (note the **query string** to filter),
   - returns the list of todos as Python objects.
2. Write code that uses it for `user_id = 1` and prints:
   - the total number of todos for that user,
   - how many are `completed` vs not,
   - the title of the first **incomplete** todo.
3. Handle no-internet gracefully with try/except around the request (print a friendly message).

**Expected output (example):**
```
User 1 has 20 todos
Completed: 11 | Not completed: 9
First incomplete: delectus aut autem
```

---

## Submission
Put everything in `day11_solution.py` (written answers as top comments), commit to repo `batch5-day11`, push to GitHub, and submit the link.

## Grading checklist
- [ ] Written answers present and correct
- [ ] Task 1 reads status code + parses JSON fields
- [ ] Task 2 correctly classifies status-code families
- [ ] Task 3 POSTs with a JSON body and reads a nested JSON field
- [ ] Task 4 uses a query string to filter and processes the returned list
- [ ] Network errors handled with try/except
