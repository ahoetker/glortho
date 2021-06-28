from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jwt_authentication_python_postgres.api.dependencies.settings import (
    get_settings,
)  # pytest
from jwt_authentication_python_postgres.api.routes import router as api_router
from jwt_authentication_python_postgres.core import tasks


def get_application():
    app = FastAPI(title="Postgres Thing", version="0.1.0")
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
