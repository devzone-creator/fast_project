from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from routes.categories import router as categories_router
from routes.product import router as product_router


app = FastAPI(title="Mex commerce API", description="A simple e-commerce API built with FastAPI", version="1.0.0")

""" 
User Model
class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
"""

# Product Model
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


# Jinja2 Templates
templates = Jinja2Templates(directory="templates")
# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Homepage
@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "title": "Amina Collection"
        }
    )

app.include_router(categories_router)
app.include_router(product_router)