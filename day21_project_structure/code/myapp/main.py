# myapp/main.py
# -----------------------------------------------------------
# The application entry point. It creates the FastAPI app, reads config,
# and plugs in the routers. Notice how SMALL and readable this stays -
# each concern lives in its own file.
#
# SETUP:  pip install "fastapi[standard]" pydantic-settings
# RUN (from the code/ folder):
#     fastapi dev myapp/main.py
#   or:
#     uvicorn myapp.main:app --reload
# Then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI

from .config import settings          # typed settings from .env
from .routers import users, items     # our route modules

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Plug each router into the app.
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
def root():
    # Never expose real secrets - just show that config loaded.
    return {"app": settings.app_name, "debug": settings.debug}
