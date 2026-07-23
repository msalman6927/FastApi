# Day 11 Handout — How the Web Works (Keep This!)

## The big picture: request → response
Everything on the web is a conversation between a **client** (asks) and a **server** (answers), carried by **HTTP** (the messaging rules).

**Restaurant analogy:** you = client, waiter = HTTP, kitchen = server, your order = request, the food = response.

## A REQUEST has 4 parts
1. **Method** (verb) — what action: GET/POST/PUT/PATCH/DELETE
2. **URL** — which resource: `https://api.site.com/users/5?sort=asc`
3. **Headers** — metadata (auth token, content type)
4. **Body** — data you send (with POST/PUT/PATCH), usually JSON

## A RESPONSE has 3 parts
1. **Status code** — how it went (200, 404…)
2. **Headers** — metadata
3. **Body** — the data (usually JSON)

## HTTP methods = CRUD
| Method | Action | Body? |
|--------|--------|-------|
| GET | Read | no |
| POST | Create | yes |
| PUT | Update (replace) | yes |
| PATCH | Update (partial) | yes |
| DELETE | Delete | no |

## Status code families
| Range | Meaning |
|-------|---------|
| 2xx | Success ("it worked") |
| 3xx | Redirect ("look elsewhere") |
| 4xx | **Client** error (YOU messed up) |
| 5xx | **Server** error (server messed up) |

Must-know: **200** OK · **201** Created · **400** Bad Request · **401** Unauthorized · **404** Not Found · **422** Validation error (FastAPI!) · **500** Server Error.

## JSON — the language of APIs
Looks like a Python dict, but: **double quotes only**, `true`/`false`/`null` lowercase.
| JSON | Python |
|------|--------|
| `{}` | dict |
| `[]` | list |
| `true`/`false` | True/False |
| `null` | None |

Convert: `json.dumps(obj)` = Python→JSON string · `json.loads(text)` = JSON→Python.
With `requests`: `response.json()` parses the body for you.

## Using `requests` (Python)
```python
import requests
r = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(r.status_code)     # 200
data = r.json()          # body as a Python dict
requests.post(url, json={"title": "hi"})   # send a body
```

## REST in one line
A style where **URLs are nouns** (resources: `/users/5`), **HTTP methods are the verbs**, data is **JSON**, responses carry **status codes**, and each request is **stateless** (server remembers nothing between calls).

## Your homework
`day11_solution.py`: written concept answers + code that GETs a todo, classifies status codes, POSTs a resource, and filters todos with a query string. Push to repo `batch5-day11`.

## Next class (Day 12)
**Pydantic** — how to define and *validate* data structures in Python (the same encapsulation/validation ideas from OOP Day 5). This is the essential prerequisite before we build APIs with FastAPI on Day 13.
