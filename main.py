from fastapi import FastAPI, Request, HTTPException
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from data.products import products
from data.categories import categories


app = FastAPI(title="Amina Collection")

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

# Categories route
@app.get("/categories")
async def get_categories(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={
            "request": request,
            "categories": categories
        }
    )

# Products Page
@app.get("/products")
async def get_products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "request": request,
            "products": products
        }
    )


# Single Product Page
@app.get("/products/{product_id}")
async def get_single_product( request: Request, product_id: int):

    # Search for matching product
    for product in products:

        if product["id"] == product_id:

            return templates.TemplateResponse(
                request=request,
                name="product_detail.html",
                context={
                    "request": request,
                    "product": product
                }
            )

    # If product not found
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.get("/create-product")
async def create_product_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_product.html",
        context={"request": request}
    )

@app.post("/create-product")
async def create_product(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...)
):
    new_product = {
        "id": len(products)+1,
        "name": name,
        "price": price,
        "stock": stock
    }

    products.append(new_product)

    return RedirectResponse(
        url="/products",
        status_code=303
    )

# Update : Working with Prefilled form data

@app.get("/products/{product_id}/edit")
async def edit_product_page(request: Request, product_id: int):
    for product in products:
        if product["id"] == product_id:
            return templates.TemplateResponse(
                request=request,
                name="edit_product.html",
                context={
                    "request": request,
                    "product": product
                }
            )
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.post("/products/{product_id}/edit")
async def edit_product(

    product_id: int,
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...)
):
    for product in products:
        if product["id"] == product_id:
            product["name"] = name
            product["price"] = price
            product["stock"] = stock

            return RedirectResponse(
                url=f"/products/{product_id}",
                status_code=303
            )

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.post("/products/{product_id}/delete")
async def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)

            return RedirectResponse(
                url="/products",
                status_code=303
            )
        
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )