from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from appfastapi.routers import auth_router, db_router
from fastapi.responses import HTMLResponse
from .general_data import templates
from .schemas import UserRead
from .dependencies import current_user

app = FastAPI(
    title = "Weather API"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(db_router.router)

@app.get('/', response_class=HTMLResponse)
async def root(request: Request = None, user: UserRead = Depends(current_user)):
    return templates.TemplateResponse(
        request=request, name="pages/home.html", context={
            "user": user
        }
    )