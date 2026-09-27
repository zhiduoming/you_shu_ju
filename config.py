from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 从.env中配置数据库url
    database_url: str = Field(validation_alias="DATABASE_URL")
    # 从.env中配置jwt签名
    jwt_secret_key: str = Field(validation_alias="JWT_SECRET_KEY")

    # 配置jwt过期时间
    access_token_expire_minutes: int = Field(
        default=1440,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
