from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse


web = APIRouter()

@web.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("web/favicon.ico",status_code=200)

@web.get("/", include_in_schema=False)
async def root():
    return HTMLResponse(content=open("web/index.html", encoding="UTF-8").read(),status_code=200)