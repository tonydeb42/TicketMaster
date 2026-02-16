from pydantic import BaseModel

class UploadSuccess(BaseModel):
    status: str
    message: str