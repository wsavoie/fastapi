from pydantic import BaseSettings, Field, SecretStr

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str  
    secret_key: SecretStr = Field(..., env="SECRET_KEY")
    algorithm: str
    access_token_expire_minutes: int 
    class Config:
        env_file = ".env"
settings = Settings()