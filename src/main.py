from fastapi import FastAPI, Request, Response

from src.exceptions.notfound import NotFoundException
from .routers import v1router

app = FastAPI()

app.include_router(v1router.router)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(req: Request, e: NotFoundException):
    return Response(
        status_code=404,
        content="Not found",
    )

@app.exception_handler(Exception)
async def general_exception_handler(req: Request, e: Exception):
    print(e)
    return Response(
        status_code=500,
        content="Internal server error",
    )
