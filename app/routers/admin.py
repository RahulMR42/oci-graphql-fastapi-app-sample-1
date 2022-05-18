from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.resources.graphql import graphql
from dotenv import load_dotenv
import json
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def list_attendees(request: Request):
     url = "http://sprint.rxn.graphql.us-phoenix-1.oci.customer-oci.com/graphql"
     gql_object = graphql(url)
     query_for_list_students = """query listStudents {  
     listSimpleStudents {name}
     }"""
     query_result = gql_object.query(query_for_list_students)
     return templates.TemplateResponse("admin.html", {"request": request, 'query_result': json.dumps(query_result, indent=2)})

@router.post("/admin", response_class=HTMLResponse)
async  def admin_query(request: Request, query_text: str = Form(...)):
     print(query_text)
     url = "http://sprint.rxn.graphql.us-phoenix-1.oci.customer-oci.com/graphql"
     gql_object = graphql(url)
     admin_query_result = gql_object.query(query_text)
     return templates.TemplateResponse("admin.html", {"request": request, 'admin_query_result': json.dumps(admin_query_result, indent=2)})