import os
from fastapi import Request, APIRouter, Depends,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
     return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
def post_register(request: Request, email: str = Form(...)):
    return templates.TemplateResponse('register.html', context={'request': request, 'result': email})