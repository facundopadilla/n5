from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()

from src.core.exceptions import load_exceptions_handlers
from src.routes.base_router import base_v1
from src.settings.project import ProjectSettings

app = FastAPI(
    title="N5 Now",
    description="Administrative layout for principal database",
    debug=ProjectSettings.DEBUG,
    version=ProjectSettings.VERSION,
)


app.include_router(base_v1)

load_exceptions_handlers(app)
add_pagination(app)
