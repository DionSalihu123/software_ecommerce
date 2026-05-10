from fastapi import FastAPI
import requests

app = FastAPI()

orders = []

@app.get("/")
def home():
    return {"message": "Order Service Running"}

@app.post("/create-order")
def create_order(product_id: int):

    # 1. Call Product Service
    product_response = requests.get("http://product-service:8000/products")
    products = product_response.json()

    # 2. Find product
    selected_product = None
    for p in products:
        if p["id"] == product_id:
            selected_product = p
            break

    if not selected_product:
        return {"error": "Product not found"}

    # 3. Create order
    order = {
        "order_id": len(orders) + 1,
        "product": selected_product
    }

    orders.append(order)

    # 4. CALL Notification Service (IMPORTANT PART)
    try:
        requests.post(
            "http://notification-service:8000/notify",
            params={
                "message": f"Order #{order['order_id']} created for {selected_product['name']}"
            }
        )
    except Exception as e:
        print("Notification failed:", e)

    return {
        "message": "Order created successfully",
        "order": order
    }

@app.get("/orders")
def get_orders():
    return orders
