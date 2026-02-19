from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import Base  # tus modelos
from app.core.config import Settings

# Inicializa los settings directamente
settings = Settings()

config = context.config

# logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

DATABASE_URL = settings.database_url  # por ejemplo postgres+psycopg2://user:pass@host/db

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        url=DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()
