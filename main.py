from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="."), name="static")

# Define an Item model
class Item(BaseModel):
    id: int
    name: str
    description: str = None

# In-memory storage for items
items: Dict[int, Item] = {}

# GET: Retrieve all items
@app.get("/items/")
async def read_all_items():
    return {"items": list(items.values())}

# POST: Create multiple items
@app.post("/items/")
async def create_items(new_items: List[Item]):
    created_items = []
    for item in new_items:
        if item.id in items:
            raise HTTPException(status_code=400, detail=f"Item with ID {item.id} already exists")
        items[item.id] = item
        created_items.append(item)
    return {"message": "Items created successfully", "items": created_items}

# PUT: Update an existing item by ID
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"message": "Item updated successfully", "item": item}

# DELETE: Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted successfully"}

# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return f.read()
