from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

ENV = os.getenv("ENV", "dev")

# ==============================
# TEST ENVIRONMENT (CI/CD)
# ==============================
if ENV == "test":
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# ==============================
# PRODUCTION (Cloud SQL)
# ==============================
elif os.getenv("CLOUD_SQL_CONNECTION_NAME"):

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")

    from google.cloud.sql.connector import Connector
    import pg8000

    connector = Connector()

    def getconn():
        return connector.connect(
            CLOUD_SQL_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

# ==============================
# LOCAL DEVELOPMENT
# ==============================
else:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    DB_NAME = os.getenv("DB_NAME", "latam_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(DATABASE_URL, echo=True)

# ==============================
# SESSION
# ==============================

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
