from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/socket.io", response_class=HTMLResponse)
async def get_socket_io_docs(request: Request):
    templates: Jinja2Templates = request.app.state.templates
    return templates.TemplateResponse(
        "docs/socket/index.html",
        context={"request": request},
    )
