from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.resources.graphql import graphql
from dotenv import load_dotenv
import json
import os
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def list_attendees(request: Request):
     url = os.environ['graphql_endpoint_url']
     gql_object = graphql(url)
     query_for_list_students = """query {listAteendees{fname,lname,mailid,country}}"""
     query_result = gql_object.query(query_for_list_students)
     return templates.TemplateResponse("admin.html", {"request": request, 'query_result': json.dumps(query_result, indent=2)})

@router.post("/admin", response_class=HTMLResponse)
async  def admin_query(request: Request, query_text: str = Form(...)):
     url = os.environ['graphql_endpoint_url']
     gql_object = graphql(url)
     admin_query_result = gql_object.query(f"""{query_text}""")
     print(json.dumps(admin_query_result))
     return templates.TemplateResponse("admin.html", {"request": request, 'admin_query_result': json.dumps(admin_query_result, indent=2)})