from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    
class ScenesResponse(BaseModel):
    scenes: list[str]