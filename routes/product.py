from fastapi import APIRouter, HTTPException, Request
from fastapi import Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from data.products import products
from utils.productUtils import search_product


router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Products Page
@router.get("/products")
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
@router.get("/products/{product_id}")
async def get_single_product( request: Request, product_id: int):

    # Search for matching product
    product = search_product(product_id)
    if not product:
        # If product not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={
            "request": request,
            "product": product
        }
    )

@router.get("/create-product")
async def create_product_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_product.html",
        context={"request": request}
    )


@router.post("/create-product")
async def create_product(
    
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

@router.get("/products/{product_id}/edit")
async def edit_product_page(request: Request, product_id: int):
    # Search for matching product
    product = search_product(product_id)
    if not product:
        # If product not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    return templates.TemplateResponse(
        request=request,
        name="edit_product.html",
        context={
            "request": request,
            "product": product
        }
    )

@router.post("/products/{product_id}/edit")
async def edit_product(

    product_id: int,
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...)
):
    product = search_product(product_id)
    if not product:
        # If product not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    product["name"] = name
    product["price"] = price
    product["stock"] = stock

    return RedirectResponse(
        url="/products",
        status_code=303
    )


@router.post("/products/{product_id}/delete")
async def delete_product(product_id: int):
    product = search_product(product_id)
    if not product:
        # If product not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    products.remove(product)

    return RedirectResponse(
        url="/products",
        status_code=303
    )
