from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ScenesResponse(BaseModel):
    scenes: list[str]


class MetricsResponse(BaseModel):
    threshold: int
    changedPixels: int
    totalPixels: int
    changeRatio: float
    note: str
