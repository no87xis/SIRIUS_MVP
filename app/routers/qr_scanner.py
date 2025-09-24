# MVP: QR-функционал полностью отключен
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db import get_db
from ..services.auth import get_current_user_optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/qr-scanner", response_class=HTMLResponse)
async def qr_scanner_page(request: Request, db: Session = Depends(get_db)):
    """MVP: QR-сканер отключен"""
    return RedirectResponse(url="/admin?error=QR-функционал отключен в MVP", status_code=302)


@router.get("/o/{qr_token}", response_class=HTMLResponse)
async def qr_public_order(request: Request, qr_token: str, db: Session = Depends(get_db)):
    """MVP: Публичные QR ссылки отключены"""
    return RedirectResponse(url="/shop?error=QR-функционал отключен в MVP", status_code=302)