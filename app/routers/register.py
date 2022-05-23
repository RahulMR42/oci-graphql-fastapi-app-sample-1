import json
from fastapi import Request, APIRouter, Depends,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.resources.graphql import graphql

from dotenv import load_dotenv
load_dotenv()



templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
     return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, email: str = Form(...),
                  fname: str = Form(...),
                  lname: str = Form(...),
                  country: str = Form(...),
                  pwd: str = Form(...)
                  ):
    url = "http://iehh5vzwre6z5kja.rxn.graphql.us-phoenix-1.oci.customer-oci.com/graphql"
    mutation_add_attendees="""mutation{
                                    createAteendees(input:
                                    {fname:"%s",lname:"%s",mailid:"%s",country:"%s",pwd:"%s"})
                                    {fname lname}}""" %(fname,lname,email,country,pwd)
    gql_object = graphql(url)
    add_attendees_result = gql_object.mutation(mutation_add_attendees)
    mutation_add_attendees=mutation_add_attendees.replace(pwd,"****")
    if (add_attendees_result['data']['createAteendees'] == None ):
        status = "Error"
        message = "New user registration failed!"
        details = add_attendees_result['errors'][0]['message']
        print(json.dumps(add_attendees_result))
        return templates.TemplateResponse('register.html', context={'request': request, 'status': status,'message':message,'details':details,'mutation_add_attendees':mutation_add_attendees})
    else:
        status = "Success"
        sid="""
                    query {
                        listSessions{
                        sid
                        
                         }
                        }
        """
        session_query_result=gql_object.query(sid)
        session_ids = session_query_result['data']['listSessions']
        session_mutation= """mutation add_session{
                        createAteendees_sessions(input:{mailid:"%s",sessions_ids:"%s"}){
                        mailid
                        }}""" %(email,session_ids)

        print(session_mutation)
        add_attendees_session = gql_object.mutation(session_mutation)
        session_mutation=session_mutation.split("sessions_ids")[0]  + "sessions_ids:[***]}){}"
        print(add_attendees_session)
        return templates.TemplateResponse('sessions.html', context={'status':status,'request': request, 'fname': fname,'lname':lname,
                                                                    'mutation_add_attendees':mutation_add_attendees,'scategory':sid,
                                                                    'mutate_attendees_sessions':session_mutation})