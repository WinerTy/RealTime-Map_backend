from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.app.templating import TemplateManager

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/socket.io", response_class=HTMLResponse)
async def get_socket_io_docs(request: Request):
    templates: "TemplateManager" = request.app.state.templates
    return templates.engine.TemplateResponse(
        "docs/socket/index.html",
        context={"request": request},
    )
