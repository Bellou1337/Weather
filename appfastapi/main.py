from fastapi import FastAPI
from .routers import auth, db_router

app = FastAPI(
    title = "Weather API"
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(db_router.router)

@app.get('/')
async def root():
    return {'message': 'Hello World'}