from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Cyberpunk 2077", "price": 50},
    {"id": 2, "name": "Minecraft", "price": 30}
]

@app.get("/")
def home():
    return {"message": "Product Service Running"}

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def add_product(name: str, price: float):
    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }
