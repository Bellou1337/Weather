from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from appfastapi.routers import auth_router, db_router

app = FastAPI(
    title="Weather API"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(db_router.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}
