from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from appfastapi.database import User, get_user_db
from appfastapi.config import config
from appfastapi.smtp import SMTPSender

SECRET = "mycrutoisecret"

smtp_sender = SMTPSender(config["SMTP"]["server"], config["SMTP"]["port"], config["SMTP"]["email"], config["SMTP"]["password"])

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(self, user: User, request = Optional[Request], response = None):
        smtp_sender.sendmail(user.email, "Вы вошли", "Вы вкурся, что зашлогинились на нашем крутом сайте?")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)