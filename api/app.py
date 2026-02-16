from fastapi import FastAPI
from api.upload import upload_router
from api.ticket import ticket_router
from api.departments import department_router

app = FastAPI()

app.include_router(upload_router, prefix="/upload")
app.include_router(ticket_router, prefix="/tickets")
app.include_router(department_router, prefix="/departments")