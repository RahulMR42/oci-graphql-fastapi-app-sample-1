from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.resources.graphql import graphql

import json

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/login", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.post("/login", response_class=HTMLResponse)
async def post_login(request:Request,
                     email: str = Form(...),
                     pwd: str = Form(...)
                     ):
    url = "http://iehh5vzwre6z5kja.rxn.graphql.us-phoenix-1.oci.customer-oci.com/graphql"
    login_query="""query{
                    getAteendees(mailid:"%s"){
                        fname
                        lname
                        pwd
                        }
                    }""" %(email)
    gql_object = graphql(url)
    login_query_result = gql_object.query(login_query)
    login_query=login_query.replace(pwd,"****")
    if (login_query_result['data']['getAteendees'] == None) :
        status =  "Invalid"
        message = "Invalid credentials,please recheck"
        return templates.TemplateResponse('login.html', context={'request': request,'status': status,'message': message,'login_query':login_query})
    elif (login_query_result['data']['getAteendees']['pwd'] != pwd):
        status = "Wrong"
        message = "Wrong password"
        return templates.TemplateResponse('login.html', context={'request': request,'status': status,'message': message,'login_query':login_query})
    else :
        status = "Success"
        fname = login_query_result['data']['getAteendees']['fname']
        lname = login_query_result['data']['getAteendees']['lname']
        return templates.TemplateResponse('sessions.html', context={'status':status,'request': request, 'fname': fname,'lname':lname,'mutation_add_attendees':login_query})





