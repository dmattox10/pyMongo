from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get MongoDB connection details from environment variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_ADDR = os.getenv("MONGO_ADDR")

# Construct MongoDB connection URL
MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_ADDR}/?retryWrites=true&w=majority&authSource=admin"

# Database and Collection names
DATABASE_NAME = "your-database"
COLLECTION_NAME = "your-collection"

# Model for your data
class Item(BaseModel):
    name: str
    description: str
    price: float

# Connect to MongoDB
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.mongodb = app.mongodb_client[DATABASE_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# CRUD endpoints
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_dict = item.dict()
    result = await app.mongodb[COLLECTION_NAME].insert_one(item_dict)
    if result.inserted_id:
        return item
    raise HTTPException(status_code=400, detail="Failed to create item")

@app.get("/items/", response_model=List[Item])
async def list_items():
    items = []
    cursor = app.mongodb[COLLECTION_NAME].find({})
    async for document in cursor:
        items.append(Item(**document))
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    from bson import ObjectId
    item = await app.mongodb[COLLECTION_NAME].find_one({"_id": ObjectId(item_id)})
    if item:
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    from bson import ObjectId
    result = await app.mongodb[COLLECTION_NAME].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict()}
    )
    if result.modified_count:
        return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    from bson import ObjectId
    result = await app.mongodb[COLLECTION_NAME].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found") 