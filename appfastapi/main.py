from fastapi import FastAPI
from appfastapi.routers import auth_router, db_router

app = FastAPI(
    title = "Weather API"
)

app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(db_router.router)

@app.get('/')
async def root():
    return {'message': 'Hello World'}