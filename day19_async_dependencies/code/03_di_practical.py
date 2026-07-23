# 03_di_practical.py
# -----------------------------------------------------------
# GOAL: Two practical dependency patterns:
#   1) an API-key check that GUARDS routes (raises 401) - preview of Day 20 auth
#   2) a `yield` dependency that manages a resource (setup + cleanup)
#
# RUN:  fastapi dev 03_di_practical.py  ->  /docs
# TEST the secure route with header:  x-api-key: secret123
# -----------------------------------------------------------

from fastapi import FastAPI, Depends, Header, HTTPException, status

app = FastAPI()


# ---- 1) A GUARD dependency: runs before the route, can block it ----
def verify_api_key(x_api_key: str = Header(...)):
    # Header(...) means the request MUST include an "x-api-key" header.
    if x_api_key != "secret123":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or missing API key")
    return x_api_key


# This route is protected: verify_api_key runs first. Bad key -> 401, and the
# route body never runs. (In /docs, click "Authorize" or add the header.)
@app.get("/secure-data")
def secure_data(api_key: str = Depends(verify_api_key)):
    return {"data": "top secret", "authenticated_with": api_key}


# You can also attach guards WITHOUT needing the return value:
@app.get("/admin", dependencies=[Depends(verify_api_key)])
def admin_panel():
    return {"panel": "admin"}


# ---- 2) A `yield` dependency: setup -> yield -> cleanup after response ----
class FakeConnection:
    def __init__(self):
        print("[dep] opening connection")
    def query(self):
        return ["row1", "row2"]
    def close(self):
        print("[dep] closing connection")


def get_connection():
    conn = FakeConnection()      # SETUP (before yield)
    try:
        yield conn               # injected into the route
    finally:
        conn.close()             # CLEANUP (after the response is sent)


@app.get("/rows")
def get_rows(conn: FakeConnection = Depends(get_connection)):
    return {"rows": conn.query()}
    # watch the terminal: "opening" runs before, "closing" runs after.


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
