from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.resources.graphql import graphql
from dotenv import load_dotenv
import json
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def register(request: Request):
     url = "http://sprint.rxn.graphql.us-phoenix-1.oci.customer-oci.com/graphql"
     gql_object = graphql(url)
     query_for_list_students = """query listStudents {  
     listSimpleStudents {name}
     }"""
     query_result = gql_object.query(query_for_list_students)
     return templates.TemplateResponse("admin.html", {"request": request, 'query_result': json.dumps(query_result, indent=2)})

#
# @router.post("/register", response_class=HTMLResponse)
# def post_register(request: Request, email: str = Form(...)):
#     return templates.TemplateResponse('register.html', context={'request': request, 'result': email})