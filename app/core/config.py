from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Variables obligatorias (se cargan de las env-vars de Cloud Run o .env)
    db_user: str
    db_pass: str
    db_name: str
    
    # Variables con valores por defecto para desarrollo local
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    
    cloud_sql_connection_name: Optional[str] = None

    @property
    def database_url(self) -> str:
        """
        Genera dinámicamente la URL de conexión.
        Si detecta cloud_sql_connection_name, usa el Unix Socket de GCP.
        """
        if self.cloud_sql_connection_name:
            return (
                f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@/{self.db_name}"
                f"?host=/cloudsql/{self.cloud_sql_connection_name}"
            )
        else:
            return (
                f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )

    class Config:
        env_file = ".env"
        extra = "ignore" 