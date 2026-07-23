# 03_path_and_query_together.py
# -----------------------------------------------------------
# GOAL: Combine PATH params (identify a resource) with QUERY params
# (configure the request) in one route.
#
# FastAPI decides which is which BY NAME:
#   - name appears in {} in the path -> path parameter
#   - otherwise                      -> query parameter
#
# RUN:  fastapi dev 03_path_and_query_together.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI

app = FastAPI()

# Fake data: each user has a list of orders.
ORDERS = {
    1: [{"id": 101, "status": "shipped"}, {"id": 102, "status": "pending"}],
    2: [{"id": 201, "status": "shipped"}, {"id": 202, "status": "shipped"}],
}


# user_id is a PATH param (it's in {}). status and limit are QUERY params.
@app.get("/users/{user_id}/orders")
def user_orders(user_id: int, status: str = "all", limit: int = 20):
    # /users/1/orders                       -> all orders for user 1
    # /users/1/orders?status=shipped        -> only shipped
    # /users/2/orders?status=shipped&limit=1-> shipped, at most 1
    orders = ORDERS.get(user_id, [])

    if status != "all":
        orders = [o for o in orders if o["status"] == status]

    return {
        "user_id": user_id,          # from the PATH
        "status": status,            # from the QUERY
        "limit": limit,              # from the QUERY
        "orders": orders[:limit],
    }


# Reads naturally: "user 1's orders, filtered to shipped, at most 1".
# PATH = which resource. QUERY = how you want it.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
