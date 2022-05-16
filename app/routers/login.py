from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/login", response_class=HTMLResponse)
def form_get(request: Request):
    key = os.getenv("unsplash_key")
    print(key)
    result = "Type a number"
    return templates.TemplateResponse('login.html', context={'request': request, 'result': result})


@router.post("/login", response_class=HTMLResponse)
def form_post1(request: Request, email: str = Form(...)):
    return templates.TemplateResponse('login.html', context={'request': request, 'result': email})


