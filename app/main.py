from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.user_routes import router as user_router
from app.db.database import engine
from app.db.models import Base

import logging


# -----------------------------
# Logging configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------
# FastAPI App Initialization
# -----------------------------
app = FastAPI(
    title="LATAM User Management API",
    description="User management REST API for LATAM Airlines challenge",
    version="1.0.0"
)


# -----------------------------
# Mount Static Files
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Application started successfully")


# -----------------------------
# Root Endpoint (Landing Page)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>LATAM User API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 100px;
                    background-color: white;
                }
                img {
                    width: 250px;
                }
                a {
                    display: inline-block;
                    margin-top: 30px;
                    padding: 12px 24px;
                    background-color: #c8102e;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                a:hover {
                    background-color: #a50e26;
                }
            </style>
        </head>
        <body>
            <img src="/static/logo.png" alt="LATAM Logo"/>
            <h1>LATAM User Management API</h1>
            <p>Welcome to the REST API</p>
            <a href="/docs">Go to API Documentation</a>
        </body>
    </html>
    """


# -----------------------------
# Include Routers
# -----------------------------
app.include_router(user_router, prefix="/users")
