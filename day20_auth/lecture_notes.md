# Day 20 — Authentication (API Keys & JWT Intro)

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Day 19 (dependencies), Days 11–18

> Where we are: Your API is open to anyone. Real APIs must know **who** is calling and **whether they're allowed**. Today: two levels — simple **API keys** (a shared secret) and **JWT** (JSON Web Tokens, the standard for user login). Both are built on the **dependency** pattern from yesterday. This also matters for agents later: when your agent calls tools/APIs, it authenticates the same way.
>
> **Instructor note:** Keep JWT digestible — the concept (a signed, stateless token proving identity) matters more than crypto internals. Stress one security rule loudly: **never store plaintext passwords**.

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## 1.1 Authentication vs Authorization
- **Authentication (authN):** *who are you?* (proving identity — password, token, key).
- **Authorization (authZ):** *what are you allowed to do?* (permissions/roles).
First you authenticate, then you authorize. Today focuses on authentication (with a taste of authZ via "current user").

## 1.2 Why HTTP needs tokens: statelessness
Recall Day 11: HTTP is **stateless** — the server doesn't remember you between requests. So identity must be **proven on every request**, by sending a credential (an API key or a token) in the request **headers**. That's the core mechanic of all web auth.

## 1.3 Level 1 — API keys (simplest)
A shared secret string the client sends in a header (e.g., `X-API-Key: secret123`). The server checks it via a **dependency** (yesterday's `verify_api_key`). Good for **service-to-service** access (one program calling another), not for individual human users.
- Pros: dead simple.
- Cons: one shared secret; no per-user identity; if leaked, revoke and rotate.
You already wrote this on Day 19 — today we formalize it and contrast with JWT.

## 1.4 Level 2 — JWT (JSON Web Tokens) for user login
For **users** logging in with username/password, we issue a **JWT** — a signed token the client stores and sends on each request.

**A JWT has three parts** (`header.payload.signature`, base64, dot-separated):
- **Header:** the algorithm (e.g., HS256).
- **Payload (claims):** data like `{"sub": "ayesha", "exp": <expiry>}` — the user id and expiry. **Readable by anyone** (not encrypted) — never put secrets in it.
- **Signature:** a cryptographic signature made with a **secret key only the server knows**. It proves the token wasn't tampered with.

**Why it's powerful (stateless):** the server doesn't store sessions. It just **verifies the signature** with its secret key. If valid and unexpired, the user is authenticated. Tamper with the payload → signature check fails → rejected.

**The flow:**
1. Client sends username + password to `POST /login`.
2. Server verifies them, then **creates a JWT** containing the user id + expiry, signed with the server's secret.
3. Client stores the token and sends it on every request: `Authorization: Bearer <token>`.
4. A dependency **decodes + verifies** the token on protected routes and identifies the user.

## 1.5 Passwords: the non-negotiable rule
**Never store or compare plaintext passwords.** Store a **hash** (a one-way scrambled version). On login, hash the submitted password and compare hashes. Use a proven library:
```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd.hash("mypassword")            # store THIS, never the plaintext
pwd.verify("mypassword", hashed)           # True (checks without un-hashing)
```
Hashing is one-way — even you can't recover the original. If your DB leaks, passwords stay protected. Say this twice; it's the most important security habit.

## 1.6 Creating & verifying a JWT (PyJWT)
```python
import jwt                      # pip install pyjwt
from datetime import datetime, timedelta, timezone

SECRET = "CHANGE-ME-long-random-secret"   # keep in .env, never in code (Day 21)
ALGO = "HS256"

def create_token(username: str):
    payload = {"sub": username,
               "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGO])   # raises if invalid/expired
```
- `exp` gives tokens a lifetime (so a stolen token eventually dies).
- `jwt.decode` verifies the signature and expiry; on failure it raises — catch it and return 401.

## 1.7 Protecting routes with `OAuth2PasswordBearer`
FastAPI provides `OAuth2PasswordBearer` to extract the `Authorization: Bearer <token>` header and integrate with `/docs` (an "Authorize" button appears).
```python
from fastapi.security import OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")
    return payload["sub"]        # the username

@app.get("/me")
def me(user: str = Depends(get_current_user)):
    return {"user": user}
```
`get_current_user` is just a **dependency** (Day 19) — that's why yesterday came first. Any route that adds it becomes protected and knows who's calling.

## 1.8 Common mistakes
1. **Storing plaintext passwords** — always hash.
2. **Hardcoding the JWT secret in code** — put it in `.env` (Day 21); a leaked secret lets anyone forge tokens.
3. **Putting secrets in the JWT payload** — it's readable by anyone; only put non-sensitive identifiers.
4. **No expiry (`exp`)** — tokens live forever if stolen. Always set one.
5. **Confusing authN and authZ** — logging in ≠ being allowed to do everything.
6. **Returning 200 on auth failure** — use 401 (unauthenticated) / 403 (forbidden).
7. Using HS256 secret that's short/guessable — use a long random secret.

## 1.9 Tricky questions
- **"Is a JWT encrypted?"** No — it's *signed*, not encrypted. The payload is readable (base64). Don't store secrets in it; the signature just proves it's authentic and untampered.
- **"Why not store sessions server-side?"** You can (sessions), but JWT is **stateless** — no server storage, scales easily, great for APIs and microservices.
- **"API key or JWT?"** API key for service-to-service/simple cases; JWT for user login with identity + expiry.
- **"Where does the client keep the token?"** Browser: httpOnly cookie or memory (not localStorage ideally). Scripts/agents: in a variable/secret store.
- **"401 vs 403?"** 401 = not authenticated (no/invalid credentials). 403 = authenticated but not allowed.

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + hook | Stateless HTTP → prove identity every request. authN vs authZ. |
| 10–30 | API key auth (live) | `code/01_api_key_auth.py`: header + dependency; when to use. |
| 30–45 | Passwords & hashing | `code/02_jwt_auth.py` (hashing part): never store plaintext; passlib demo. |
| 45–80 | JWT login + protect (live) | `code/02_jwt_auth.py`: `/login` issues token; `get_current_user`; `/me`, `/protected`. Use `/docs` "Authorize". |
| 80–100 | Full mini secure API | `code/03_secure_api.py`: register/login/protected CRUD. |
| 100–112 | Assignment brief | Walk through assignment. |
| 112–120 | Q&A / buffer | Preview Day 21 (project structure, .env for the secret). |

**Tip:** the memorable moment is logging in via `/docs`, copying the token into "Authorize", and watching a 401 route become 200. Also hammer the "never store plaintext passwords" rule.

---

# PART 3 — CODE FILES (`code/`)
1. `01_api_key_auth.py` — API-key header auth via a dependency.
2. `02_jwt_auth.py` — password hashing, `/login` issuing a JWT, `get_current_user`, protected routes.
3. `03_secure_api.py` — a small register/login + protected notes API tying it together.

**Install:** `pip install "fastapi[standard]" pyjwt "passlib[bcrypt]"`
**Run:** `fastapi dev 02_jwt_auth.py` → `/docs` → "Authorize".

---

# PART 4 — STUDENT HANDOUT (recap)
- **authN** = who are you; **authZ** = what you can do. HTTP is stateless → prove identity **every request** via a header.
- **API key** = shared secret in a header (service-to-service). **JWT** = signed token for user login: `header.payload.signature`, stateless, verified with a server secret.
- JWT flow: `POST /login` (verify user) → server issues token → client sends `Authorization: Bearer <token>` → `get_current_user` dependency verifies it.
- **NEVER store plaintext passwords** — hash with bcrypt (`passlib`). JWT payload is readable — no secrets inside; always set an `exp`.
- Auth is built on **dependencies** (Day 19). Secret goes in `.env` (Day 21).
- Homework: JWT login + protected routes. Push to `batch5-day20`.
- **Next (Day 21):** project structure — routers, folders, `.env` config (where the JWT secret belongs).
