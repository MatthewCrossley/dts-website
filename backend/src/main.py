import logging
import sys

from fastapi import FastAPI
from users.api import router as users_router
from db import startup as db_startup


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )
)
logger.addHandler(handler)


app = FastAPI(
    debug=True,
    title="TODO-Backend",
    description="Backend for TODO app",
    version="0.1.0",
)
app.include_router(users_router)


@app.on_event("startup")
def startup():
    logger.info("Starting up...")
    db_startup()
    logger.info("Startup complete.")
