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
        return templates.TemplateResponse('register.html', context={'request': request, 'status': status,'message':message,'details':details,'mutation_add_attendees':mutation_add_attendees})
    else:
        status = "Success"
        scategory="""
                    query {
                        listSessions{
                        scategory,
                        sname
                         }
                        }
        """
        session_query_result=gql_object.query(scategory)
        print(json.dumps(session_query_result))
        session_table='<table>\n<tbody>\n<tr><td>Devops        </td><td>OCI Devops Intro      </td></tr>\n<tr><td>Openworld     </td><td>Openworld-S1          </td></tr>\n<tr><td>AutonomousDB  </td><td>Power of autonomous DB</td></tr>\n<tr><td>AI            </td><td>OCI AI deep view      </td></tr>\n<tr><td>Devops        </td><td>OCI DevSecops         </td></tr>\n<tr><td>Openworld     </td><td>Welcome to openworld  </td></tr>\n<tr><td>Openworld     </td><td>Openworld-S2          </td></tr>\n<tr><td>UserExperience</td><td>Interactive CLI       </td></tr>\n</tbody>\n</table>'
        return templates.TemplateResponse('sessions.html', context={'status':status,'request': request, 'fname': fname,'lname':lname,
                                                                    'mutation_add_attendees':mutation_add_attendees,'scategory':scategory,
                                                                    'session_table':session_table})