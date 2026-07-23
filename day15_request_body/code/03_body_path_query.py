# 03_body_path_query.py
# -----------------------------------------------------------
# GOAL: Use PATH + BODY + QUERY parameters together in one endpoint.
# FastAPI decides which is which by how each parameter is declared:
#   - name in {}            -> PATH parameter
#   - Pydantic model type   -> request BODY
#   - other simple type     -> QUERY parameter
#
# RUN:  fastapi dev 03_body_path_query.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Review(BaseModel):
    rating: int
    comment: str


# One endpoint, three kinds of input:
#   product_id -> PATH (in {})
#   review     -> BODY (Pydantic model)
#   notify     -> QUERY (simple type, has a default => optional)
@app.post("/products/{product_id}/reviews")
def add_review(product_id: int, review: Review, notify: bool = False):
    return {
        "product_id": product_id,     # from the URL path
        "review": review,             # from the JSON body
        "notify_seller": notify,      # from the query string
    }


# Example request (send via /docs):
#   POST /products/7/reviews?notify=true
#   body: {"rating": 5, "comment": "Great product!"}
#
# Result combines all three sources of input cleanly.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
