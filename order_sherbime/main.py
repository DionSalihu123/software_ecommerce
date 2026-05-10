from fastapi import FastAPI
import requests

app = FastAPI()

orders = []

@app.get("/")
def home():
    return {"message": "Order Service Running"}

@app.post("/create-order")
def create_order(product_id: int):

    # Call Product Service
    response = requests.get("http://product-service:8000/products")

    products = response.json()

    # Find product
    selected_product = None

    for product in products:
        if product["id"] == product_id:
            selected_product = product
            break

    if not selected_product:
        return {"error": "Product not found"}

    order = {
        "order_id": len(orders) + 1,
        "product": selected_product
    }

    orders.append(order)

    return {
        "message": "Order created successfully",
        "order": order
    }

@app.get("/orders")
def get_orders():
    return orders
