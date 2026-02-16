from pydantic import BaseModel

class TicketRequest(BaseModel):
    query:str
    department:str