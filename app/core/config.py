from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    DEBUG: bool

    HOST: str
    PORT: int

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    MAIL_CC: str
    MAIL_BCC: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property
    def MAIL_CC_LIST(self) -> list[str]:

        if not self.MAIL_CC:
            return []

        return [
            x.strip()
            for x in self.MAIL_CC.split(",")
            if x.strip()
        ]


    @property
    def MAIL_BCC_LIST(self) -> list[str]:

        if not self.MAIL_BCC:
            return []

        return [
            x.strip()
            for x in self.MAIL_BCC.split(",")
            if x.strip()
        ]


settings = Settings()