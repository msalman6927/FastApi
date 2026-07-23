# Day 20 Assignment — Authentication

**Module 02 · Day 20**
**Goal:** Protect an API with an API key, then implement JWT login with hashed passwords and protected routes.

> `pip install "fastapi[standard]" pyjwt "passlib[bcrypt]"`

---

## Task 1 (Easy) — API key
1. Create a `require_key` dependency checking an `X-API-Key` header against a constant.
2. One public route and one protected route.
3. Test with and without the correct header (expect 401 when wrong).

---

## Task 2 (Medium) — Password hashing
1. Using `passlib` (bcrypt), write a tiny script or route that hashes a password and verifies it.
2. In a comment, explain WHY we never store plaintext passwords.

---

## Task 3 (Medium) — JWT login
1. A fake user store with one user whose password is **hashed**.
2. `POST /login` (use `OAuth2PasswordRequestForm`) that verifies credentials and returns a JWT (`access_token`, `token_type`).
3. A `get_current_user` dependency that decodes/verifies the token (401 on failure).
4. Protect `GET /me` to return the current username.

---

## Task 4 (Challenge) — Secure per-user resource
1. Add `POST /register` (hash the password, 409 if username taken).
2. Add a per-user resource (e.g., `/tasks`): each logged-in user can list and add only **their own** tasks.
3. Ensure tokens expire (`exp`) and the JWT secret is read from an environment variable (or clearly marked TODO for `.env` on Day 21).

---

## Submission
`auth_app.py` → repo `batch5-day20` with a README (list the install commands + test steps).

## Checklist
- [ ] API-key dependency returns 401 on bad key
- [ ] Passwords hashed with bcrypt (never plaintext)
- [ ] `/login` issues a JWT; `get_current_user` verifies it
- [ ] Protected routes return 401 without a valid token
- [ ] Per-user data isolation (each user sees only their own)
- [ ] Token has an expiry
