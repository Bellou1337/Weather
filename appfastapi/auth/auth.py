from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers
from appfastapi.database import User
from .manager import get_user_manager

cookie_transport = CookieTransport(cookie_max_age=3600)
SECRET = "f1e9ec2d84e898724cd2838a5b04316f8497b4e5cc4209bde9b02fceb866449f"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)



auth_backend = AuthenticationBackend(
    name="auth",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)