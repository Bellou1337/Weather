from appfastapi.auth import fastapi_users
from appfastapi.auth import auth_backend
from appfastapi.schemas import UserCreate, UserRead, UserUpdate
from appfastapi.auth.manager import get_user_manager, UserManager
from appfastapi.general_data import templates

from fastapi import APIRouter, Query, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi_users import schemas, exceptions
from fastapi_users.router.common import ErrorCode

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix="/jwt"
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

@router.get(
    "/verify",
    name="verify:verify",
    response_class=HTMLResponse
)
async def verify(
    request: Request,
    token: str = Query(str),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(token, request)
        return templates.TemplateResponse(
            request=request, name="pages/verification.html", context={
                "user": schemas.model_validate(UserRead, user),
                "status": "OK"
            }
        )
    except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
        return templates.TemplateResponse(
            request=request, name="pages/verification.html", context={
                "status": ErrorCode.VERIFY_USER_BAD_TOKEN
            }
        )
    except exceptions.UserAlreadyVerified:
        return templates.TemplateResponse(
            request=request, name="pages/verification.html", context={
                "status": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
            }
        )

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)