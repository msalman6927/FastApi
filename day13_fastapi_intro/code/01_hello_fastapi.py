# 01_hello_fastapi.py
# -----------------------------------------------------------
# GOAL: The smallest possible FastAPI app. Run it, and you have a live API.
#
# SETUP:  pip install "fastapi[standard]"
# RUN (recommended, auto-reload):
#     fastapi dev 01_hello_fastapi.py
# RUN (classic):
#     uvicorn 01_hello_fastapi:app --reload
# RUN (simplest, no reload):
#     python 01_hello_fastapi.py
#
# Then open in a browser:
#     http://127.0.0.1:8000/          -> your JSON
#     http://127.0.0.1:8000/docs      -> interactive Swagger docs
# Stop the server with Ctrl + C.
# -----------------------------------------------------------

from fastapi import FastAPI

# 1) Create the application object. The name `app` matters:
#    the server runs THIS object (uvicorn 01_hello_fastapi:app).
app = FastAPI()


# 2) A "path operation": handle GET requests to the path "/".
#    @app.get("/") registers the function below as the handler.
@app.get("/")
def read_root():
    # 3) Return a Python dict -> FastAPI converts it to JSON automatically,
    #    with status code 200. No json.dumps needed.
    return {"message": "Hello, Batch 5! Your first API is live."}


# A second route so there's more than one thing to see.
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---- Fallback so `python 01_hello_fastapi.py` also starts the server ----
# (For live-reload during development, prefer `fastapi dev 01_hello_fastapi.py`.)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
