from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="far_api")

# Pydantic Models for request/response
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    quantity: int

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class IemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# In memory database

items_db = []
counter = 1


@app.get("/")
async def root():
    return {"message": "Welcome to fast python"}


# Create
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: itemCreate):
    global counter
    new_item = Item(id=counter, **item.dict())
    items_db.append(new_item)
    counter += 1
    return new_item


# READ all items
@app.get("/items/", response_model=List[Item])
async def read_items():
    return items_db

# READ single item
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item















"""
@app.post("/login")
async def login():
    return {"token": "abc123"}

@app.get("/users")
async def get_users():
    return [{"id": 1,"name": "Alice"},
        {"id": 2,"name": "Bob"},
        {"id": 3,"name": "Charlie"},
        {"id": 4,"name": "David"},
        {"id": 5,"name": "Eve"}
    ]

@app.post("/users")
async def create_user():
    return {"id": 2, "name": "Bob"}
"""