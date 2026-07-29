from fastapi import FastAPI

from api.routers import health, scenes


app = FastAPI(title="SAR Change Review Workbench API")

app.include_router(health.router)
app.include_router(scenes.router)