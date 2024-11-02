from fastapi.templating import Jinja2Templates
from appfastapi.config import config

templates = Jinja2Templates(directory="templates")

SECRET = config["Miscellaneous"]["Secret"]