from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates("templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Render Home Page"
)
def root(request: Request):
    """
    Renderiza el archivo templates/index.html
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={ }
    )