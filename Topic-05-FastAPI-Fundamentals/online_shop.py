from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="My Online-Shop API",
    description="A simple FastAPI application",
    version="1.0.0"
)

# Define a route
@app.get("/")
async def homepage():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}