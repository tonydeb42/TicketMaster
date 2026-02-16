import redis
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os
from api.models.DepartmentResponse import DepartmentResponse

load_dotenv()

department_router = APIRouter()
REDIS_URL = os.getenv("REDIS_HOST", "redis://localhost:6379/2")

@department_router.get("/",response_model=DepartmentResponse)
async def get_departments():
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        departments = redis_client.smembers("departments")

        if not departments:
            raise HTTPException(status_code=404, detail="Departments not found")

        return {"departments": list(departments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))