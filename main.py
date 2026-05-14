from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to fast python"}

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