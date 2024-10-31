from typing import Optional

from fastapi import Depends, Request, BackgroundTasks
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions

from appfastapi.database import User, get_user_db
from appfastapi.config import config
from appfastapi.smtp import SMTPSender
from appfastapi.general_data import templates

SECRET = "mycrutoisecret"

smtp_sender = SMTPSender(config["SMTP"]["server"], config["SMTP"]["port"], config["SMTP"]["email"], config["SMTP"]["password"])

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        try:
            await self.request_verify(user, request)
        except (
            exceptions.UserNotExists,
            exceptions.UserInactive,
            exceptions.UserAlreadyVerified,
        ):
            pass

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        html = templates.TemplateResponse(
            request=request, name="email/verification.html", context={
                "username": user.login,
                "token": token
                }
        )
        
        smtp_sender.send_HTML_mail_task(user.email, "Вы вошли", html.body.decode())

    async def on_after_login(self, user: User, request = Optional[Request], response = None):
        pass



async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)