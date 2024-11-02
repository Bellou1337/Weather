from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers
from appfastapi.database import User
from .manager import get_user_manager
from appfastapi.general_data import SECRET
from appfastapi.config import config

TOKEN_EXPIRE = config.get("Miscellaneous", "token_expire")

cookie_transport = CookieTransport(cookie_max_age=TOKEN_EXPIRE)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=TOKEN_EXPIRE)



auth_backend = AuthenticationBackend(
    name="auth",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)