import os

workers = os.getenv("GUNICORN_WORKERS", 3)
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
limit_request_line = 0
limit_request_field_size = 0
