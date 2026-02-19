from fastapi import FastAPI
from app.api.user_routes import router as user_router
from app.db.database import engine
from app.db.models import Base
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LATAM User Management API",
    description="User management REST API for LATAM Airlines challenge",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Application started successfully")


app.include_router(user_router, prefix="/users")
