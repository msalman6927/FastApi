# Day 11 — How the Web Works (HTTP, Requests/Responses, Methods, Status Codes, JSON, REST)

**Module:** 02 — FastAPI

## 1.1 The mental model: client & server (the restaurant analogy)

The whole web is built on a **request → response** conversation between two roles:
- **Client** — the one who *asks* for something (your browser, a mobile app, a Python script, an AI agent).
- **Server** — the one who *has* the resources and *responds* (a computer somewhere running a program that listens for requests).

**Restaurant analogy (use this all lesson):**
- You (the **client**) sit at a table.
- The **waiter** is **HTTP** — the messaging protocol that carries your order to the kitchen and brings food back.
- The **kitchen** is the **server** — it does the work and prepares what you asked for.
- Your **order** ("one pizza, no olives") is the **request**.
- The **food delivered** (or "sorry, we're out of pizza") is the **response**.

You don't walk into the kitchen yourself — you send a structured order through the waiter and get a structured reply. That's exactly client ↔ HTTP ↔ server.

**Why this matters for us:** a **web API** is a kitchen that serves *data* instead of food. FastAPI (Module 3 onward) is how *you* build such a kitchen. AI agents are clients that place orders (call tools/APIs). Everything is request → response.

## 1.2 What is HTTP?

**HTTP** = **H**yper**T**ext **T**ransfer **P**rotocol. A **protocol** is just an agreed-upon set of rules for how two computers talk. HTTP defines the *format* of requests and responses so any client and any server can understand each other.

Key properties to teach:
- **Text-based & structured:** a request/response is basically structured text (a line, some headers, maybe a body).
- **Stateless:** each request is independent — the server doesn't automatically remember your previous request. (State is added later via tokens/sessions/databases. Mention now; important for auth on Day 20.)
- **HTTPS** = HTTP + encryption (the "S" = Secure/TLS). Same rules, but the messages are encrypted in transit. Always prefer HTTPS.

## 1.3 Anatomy of a REQUEST

Every HTTP request has up to four parts:

1. **Method (verb)** — *what action* you want: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
2. **URL (address)** — *what resource* and *where*: `https://api.example.com/users/5`
   - **scheme** `https://` · **host** `api.example.com` · **path** `/users/5` · optional **query string** `?sort=asc&limit=10`.
3. **Headers** — *metadata* about the request: who's asking, what format they want, auth tokens. E.g., `Content-Type: application/json`, `Authorization: Bearer <token>`.
4. **Body** (optional) — *the data you're sending* (used mainly with POST/PUT/PATCH), usually JSON. GET requests normally have no body.

Analogy: method = the *verb* of your order ("bring", "change", "cancel"); URL = *which dish*; headers = *notes* ("I'm a member", "I want it in a box"); body = *the details* of a new order.

## 1.4 Anatomy of a RESPONSE

Every response has three parts:

1. **Status code** — a 3-digit number saying *how it went* (200 OK, 404 Not Found…). See 1.6.
2. **Headers** — metadata about the response (`Content-Type: application/json`, length, caching…).
3. **Body** — *the actual data* returned, usually JSON for APIs.

The client reads the status code first ("did it work?"), then parses the body ("give me the data").

## 1.5 HTTP methods (the verbs) — and CRUD

The method tells the server what you want to *do* with a resource. The four core verbs map cleanly onto **CRUD** (Create, Read, Update, Delete) — the four basic things you do to data:

| Method | CRUD | Meaning | Has body? | Example |
|--------|------|---------|-----------|---------|
| **GET** | Read | Fetch a resource | No | get user #5 |
| **POST** | Create | Create a new resource | Yes | add a new user |
| **PUT** | Update | Replace a resource entirely | Yes | overwrite user #5 |
| **PATCH** | Update | Partially update a resource | Yes | change only user #5's email |
| **DELETE** | Delete | Remove a resource | No/optional | delete user #5 |

Two important properties (mention, don't over-drill):
- **GET should be "safe"** — it only reads, never changes data. Never make a GET that deletes something.
- **GET/PUT/DELETE are "idempotent"** — doing them twice has the same effect as once. **POST is not** — POSTing twice usually creates two resources. (This is why double-submitting a form can create duplicate orders.)

## 1.6 Status codes (how the server reports the outcome)

Status codes come in **five families** by their first digit. Teach the families first, then a few specific ones:

| Range | Family | Meaning | Memory hook |
|-------|--------|---------|-------------|
| **1xx** | Informational | "Hold on, still going" | rare, ignore for now |
| **2xx** | Success | "It worked!" | **2 = good** |
| **3xx** | Redirection | "Go look somewhere else" | moved |
| **4xx** | Client error | "**You** messed up" | your fault (bad request) |
| **5xx** | Server error | "**I** messed up" | server's fault |

The specific ones students must know:
- **200 OK** — success (GET/PUT/PATCH/DELETE worked).
- **201 Created** — success, a new resource was created (typical POST response).
- **204 No Content** — success, nothing to return (common for DELETE).
- **400 Bad Request** — your request was malformed.
- **401 Unauthorized** — you're not authenticated (no/invalid credentials).
- **403 Forbidden** — authenticated, but not allowed.
- **404 Not Found** — that resource doesn't exist.
- **422 Unprocessable Entity** — data failed validation (FastAPI returns this a lot — remember it!).
- **500 Internal Server Error** — the server crashed handling your request.

Memory aids: **4xx = you (client) did something wrong; 5xx = the server did**. "404" is culturally famous ("page not found") — anchor on it.

## 1.7 JSON — the language of APIs

**JSON** = **J**ava**S**cript **O**bject **N**otation. It's a lightweight, text-based format for structured data that *both humans and machines* read easily. It's how APIs almost always send/receive data.

JSON looks almost exactly like a Python dict/list:
```json
{
  "id": 5,
  "name": "Ayesha",
  "is_active": true,
  "roles": ["admin", "editor"],
  "profile": { "age": 25, "city": "Karachi" }
}
```
JSON ↔ Python mapping (teach this table — it's the whole trick):

| JSON | Python |
|------|--------|
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Two gotchas:
- JSON uses **double quotes only** (`"name"`, never `'name'`), `true`/`false`/`null` are lowercase.
- In Python we convert with the `json` module: `json.dumps(obj)` (Python → JSON string, "dump string") and `json.loads(text)` (JSON string → Python, "load string"). With the `requests` library, `response.json()` does the parse for you.

## 1.8 What is an API? What is REST?

**API** = **A**pplication **P**rogramming **I**nterface — a defined way for one program to talk to another. A **web API** does it over HTTP. Analogy: a **menu** in the restaurant — it lists exactly what you can order and how. You don't need to know how the kitchen cooks; you just use the menu. An API hides the internals and exposes a clean set of operations.

**REST** = **RE**presentational **S**tate **T**ransfer — the most common *style* of designing web APIs. It's a set of conventions, not a technology. The key REST ideas:
- **Everything is a "resource"** identified by a URL: `/users`, `/users/5`, `/products/12/reviews`.
- **You act on resources using HTTP methods** (the verbs above). `GET /users/5` = read user 5; `DELETE /users/5` = delete user 5. Same URL, different verb, different action.
- **Use nouns in URLs, not verbs.** `GET /users/5` ✅ not `GET /getUser?id=5` ❌. The *method* is the verb; the *URL* is the noun.
- **Stateless:** each request carries everything the server needs; the server doesn't remember previous calls.
- **Returns structured data (JSON)** and meaningful **status codes**.

A "RESTful" API is just one that follows these conventions. FastAPI makes building RESTful APIs natural — which is why we learn REST *before* FastAPI.

## 1.9 How this connects to the rest of the course (motivate it)
- **FastAPI (Days 13–22):** you'll *build* REST APIs — define resources, methods, return JSON + status codes. Today's vocabulary is exactly what those lessons use.
- **AI agents (LangGraph):** tools an agent calls are usually API requests. An agent that "searches the web" or "checks the weather" is a client making HTTP requests.
- **RAG & n8n:** both move data between services via HTTP/JSON.
Understanding request → response → status → JSON is the shared language of the whole second half of the course.



# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
