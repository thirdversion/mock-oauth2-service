from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strivelogger import StriveLogger, UvicornLogger

from .routes.additional_routes import router as additional_router
from .routes.oauth2_routes import router as oauth_router
from .settings import get_settings

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

StriveLogger.initialize(logger=UvicornLogger())
StriveLogger.info("Service started")


app.include_router(additional_router)


app.include_router(oauth_router)
