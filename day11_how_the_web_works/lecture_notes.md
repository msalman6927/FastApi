# Day 11 — How the Web Works (HTTP, Requests/Responses, Methods, Status Codes, JSON, REST)

**Module:** 02 — FastAPI
**Duration:** 2 hours
**Prerequisite:** Module 1 (OOP), Day 1 (`requests` installed)

> Where we are: We're leaving pure Python and entering the world of **web APIs** — programs that talk to other programs over the internet. This is the foundation of everything ahead: FastAPI (Module 2) *builds* APIs; LangGraph agents and RAG systems *call* APIs; n8n *connects* APIs. Today has **no FastAPI yet** — first you must deeply understand HTTP, requests/responses, status codes, JSON, and REST. We make it concrete by actually firing real HTTP requests from Python with the `requests` library and inspecting what comes back.
>
> **Instructor note:** This is one of your weaker areas, so Part 1 teaches *you* in depth — enough to answer any student question with confidence. Read it fully before class.

---

# PART 1 — INSTRUCTOR DEEP-DIVE (teach yourself first)

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

## 1.10 Common mistakes / confusions (pre-empt them)
- **Confusing URL path vs query string.** Path identifies the resource (`/users/5`); query string filters/sorts (`?limit=10`). 
- **Thinking GET can have a body.** It technically can but shouldn't — GET data goes in the query string.
- **Assuming 200 means "data exists."** A search returning an empty list is still 200; "not found" for a specific resource is 404. Different things.
- **Forgetting JSON needs double quotes.** Single quotes = invalid JSON.
- **Mixing up `json.dumps`/`json.loads`.** dumpS = to String (Python→JSON); loadS = from String (JSON→Python).
- **Believing the server "remembers" you.** HTTP is stateless; identity comes from tokens sent on *every* request (Day 20).

## 1.11 Tricky student questions & your answers

**Q: "Is HTTP the same as the internet?"**
A: No. The internet is the physical network. HTTP is *one protocol* that runs on top of it for web communication (email, video, etc. use other protocols). HTTP is how browsers and APIs talk.

**Q: "What's the difference between a website and an API?"**
A: A website returns HTML meant for *humans* to view in a browser. An API returns data (JSON) meant for *programs* to use. Same HTTP underneath; different audience and format.

**Q: "PUT vs PATCH?"**
A: PUT replaces the *whole* resource; PATCH changes *part* of it. Editing only an email → PATCH. Replacing the entire user record → PUT.

**Q: "Why 422 and not 400?"**
A: 400 = the request itself was malformed (bad syntax). 422 = syntax was fine but the *data failed validation rules* (e.g., age is negative). FastAPI + Pydantic return 422 for validation failures — you'll see it constantly.

**Q: "Do I need to memorize all status codes?"**
A: No — memorize the *families* (2/3/4/5) and a handful: 200, 201, 400, 401, 404, 422, 500. Look up the rest.

**Q: "Where does the API 'live'?"**
A: On a server — a computer running a program that listens for HTTP requests on a port. Right now those servers belong to other companies; from Day 13 *you'll* run your own on your laptop, and in the deployment module you'll put it on a real server.

**Q: "Is REST a language or a library?"**
A: Neither — it's a *style/convention* for designing APIs. You can follow REST in any language. FastAPI just makes following it easy.

---

# PART 2 — 2-HOUR LECTURE PLAN (minute-by-minute)

| Time | Segment | What you do |
|------|---------|-------------|
| **0–10 min** | **Module 2 kickoff + hook** | "We can model data with OOP; now we make programs *talk to each other over the internet*." Restaurant analogy. Show what a request/response looks like at a high level. |
| **10–30 min** | **Client/server, HTTP, request & response anatomy** | Whiteboard the request parts (method, URL, headers, body) and response parts (status, headers, body). Keep it conversational with the restaurant metaphor. |
| **30–50 min** | **First real request (live)** | `code/01_first_http_request.py`: fire a GET, print status code, a header, and the body. Make the abstract concrete — "this is a real conversation with a server across the world." |
| **50–70 min** | **Methods & status codes (live)** | `code/02_http_methods.py` and `code/03_status_codes.py`: GET vs POST; trigger 200/404 and read the families. Map methods → CRUD. |
| **70–90 min** | **JSON (live)** | `code/04_working_with_json.py`: JSON ↔ Python dict, `json.dumps`/`loads`, `response.json()`. The mapping table. |
| **90–108 min** | **REST tour (live)** | `code/05_rest_api_tour.py`: hit a real REST API doing read/create; show resource URLs + verbs + status codes together. This ties everything up. |
| **108–116 min** | **Assignment brief + recap** | Walk through `assignments/assignment.md`. Recap the request→response→status→JSON loop. |
| **116–120 min** | **Q&A / buffer** | Answer questions; preview Day 12 (Pydantic) and Day 13 (building our OWN API). |

**Timing tip:** the payoff moment is `01_first_http_request.py` (30–50) — the first time students see their Python code get a real reply from a server they don't control. Let that land ("you just talked to a computer on the other side of the world"). Everything else is elaboration. Ensure internet works beforehand; if the venue's network is unreliable, pre-run the scripts and have screenshots ready.

---

# PART 3 — CODE / DEMO FILES (in `code/`, run in this order)

1. `01_first_http_request.py` — a single GET; inspect status code, headers, and body.
2. `02_http_methods.py` — GET vs POST against a test API; methods → CRUD.
3. `03_status_codes.py` — trigger and interpret 200 / 404 / others; the families.
4. `04_working_with_json.py` — JSON ↔ Python, `json.dumps`/`loads`, `response.json()`.
5. `05_rest_api_tour.py` — a mini REST tour (resources + verbs + status) on a real public API.

**Install command needed today:**
```
pip install requests
```
(Already installed on Day 1; re-run if a student's venv is fresh.) All demos hit **free, no-auth public test APIs** (`jsonplaceholder.typicode.com`, `httpbin.org`). Internet required.

---

# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
