from pydantic import BaseModel

class TicketSuccess(BaseModel):
    status: str
    message: str