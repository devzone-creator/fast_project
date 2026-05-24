from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from data.categories import categories

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Categories route
@router.get("/categories")
async def get_categories(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={
            "request": request,
            "categories": categories
        }
    )
