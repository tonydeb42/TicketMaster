from fastapi import APIRouter, HTTPException
from api.models.TicketSuccess import TicketSuccess
from api.models.TicketRequest import TicketRequest
from dotenv import load_dotenv
import os

from celery import chain
from worker.query_transformation.metadata_extractor import extract_metadata
from worker.query_transformation.query_parser import query_parser
from worker.query_transformation.retrieve_chunks import retrieve_chunks
from worker.query_transformation.generate_answer import generate_answer
from worker.query_transformation.send_notification import send_notification
from worker.query_transformation.failure_notification import failure_notification

load_dotenv()
ticket_router = APIRouter()

email = os.getenv("NOTIFICATION_EMAIL")

@ticket_router.post("/",response_model=TicketSuccess)
async def get_tickets(req: TicketRequest):
    try:
        current_user = email

        find_employee_chain = chain(
            extract_metadata.s(req.query, req.department),
            query_parser.s(),
            retrieve_chunks.s(),
            generate_answer.s(),
            send_notification.s(current_user)
        ).apply_async(
            link_error=failure_notification.s(current_user)
        )

        return {"status": "success", "message": "Ticket creation process started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating ticket: " + str(e))