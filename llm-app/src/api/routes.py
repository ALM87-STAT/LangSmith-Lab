from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
