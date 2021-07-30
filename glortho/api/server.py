from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from glortho.api.dependencies.settings import (
    get_settings,
)  # pytest
from glortho.api.routes import router as api_router
from glortho.core import tasks


def get_application():
    app = FastAPI(title="Glortho Authentication Server", version="0.3.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))
    app.include_router(api_router, prefix="")
    return app


app = get_application()
