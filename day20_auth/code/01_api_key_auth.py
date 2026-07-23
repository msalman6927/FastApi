# 01_api_key_auth.py
# -----------------------------------------------------------
# GOAL: Simplest auth - an API key sent in a header, checked by a dependency.
# Good for service-to-service access (one program calling another).
#
# RUN:  fastapi dev 01_api_key_auth.py  ->  /docs
# TEST: add header  x-api-key: secret123
# -----------------------------------------------------------

from fastapi import FastAPI, Depends, Header, HTTPException, status

app = FastAPI()

# In real life this lives in .env (Day 21), never hardcoded.
VALID_API_KEY = "secret123"


def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or missing API key")
    return x_api_key


# Public route - no key needed.
@app.get("/public")
def public():
    return {"message": "anyone can see this"}


# Protected route - the dependency runs first; bad key -> 401.
@app.get("/private")
def private(_: str = Depends(require_api_key)):
    return {"message": "you provided a valid API key"}


# API KEY vs JWT:
#   - API key: one shared secret, no per-user identity. Simple, for services.
#   - JWT (file 02): proves WHICH USER, has an expiry. For human login.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
