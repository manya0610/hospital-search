import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.app.routers.note_router import note_router
from src.app.routers.patient_router import patient_router
from src.app.routers.public_router import public_router

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    x_api_key = request.headers.get("X-API-KEY")
    if not x_api_key or x_api_key != os.getenv("API_KEY"):
        return JSONResponse({"error": "X-API-KEY MISSING or INCORRECT"}, 401)
    response = await call_next(request)
    return response

app.include_router(note_router)
app.include_router(patient_router)
app.include_router(public_router)
