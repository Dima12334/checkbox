from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import (
    ALLOWED_HOSTS,
    ALLOWED_METHODS,
    ALLOWED_HEADERS,
    ALLOW_CREDENTIALS,
    DEBUG,
)
from src.api.v1.v1_routers import api_v1_router

app = FastAPI(debug=DEBUG, docs_url="/api/docs/", title="Checkbox challenge")
add_pagination(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


app.include_router(api_v1_router, prefix="/api")
