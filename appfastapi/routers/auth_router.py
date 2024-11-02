from appfastapi.auth import auth_backend, fastapi_users
from appfastapi.schemas import UserCreate, UserRead, UserUpdate
from appfastapi.auth.manager import get_user_manager, UserManager
from appfastapi.general_data import templates

from fastapi import APIRouter, Query, Request, Depends, HTTPException, status, Form
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

@router.get(
    "/reset-password",
    name="reset:reset_password_page",
    response_class=HTMLResponse
)
async def reset_password(
    request: Request,
    token: str = Query(...)
):
    return templates.TemplateResponse(
        request=request, name="pages/reset_password.html", context={
            "token": token
        }
    )

@router.post(
    "/reset-password_form",
    name="reset:reset_password_form"
)
async def reset_password(
    request: Request,
    token: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        await user_manager.reset_password(token, password, request)
        return templates.TemplateResponse(
            request=request, name="pages/reset_password_finish.html", context={
                "status": "OK"
            }
        )
    except (
        exceptions.InvalidResetPasswordToken,
        exceptions.UserNotExists,
        exceptions.UserInactive,
    ):
        return templates.TemplateResponse(
            request=request, name="pages/reset_password_finish.html", context={
                "status": ErrorCode.RESET_PASSWORD_BAD_TOKEN
            }
        )
    except exceptions.InvalidPasswordException as e:
        return templates.TemplateResponse(
            request=request, name="pages/reset_password_finish.html", context={
                "status": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD
            }
        )

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)