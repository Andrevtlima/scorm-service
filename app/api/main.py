
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.api.courses import router as courses_router
from app.api.registrations import router as reg_router
from app.api.launch_url import router as launch_router

app = FastAPI(title="SCORM Microservice")

app.include_router(courses_router)
app.include_router(reg_router)
app.include_router(launch_router)
app.mount("/data", StaticFiles(directory="data"), name="data")
