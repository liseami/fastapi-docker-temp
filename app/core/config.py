
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # 从.env文件读取环境变量,之所以能拿到env文件是因为docker compose yml文件里指定了env文件的位置
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # 用户欢迎信息
    USER_HOME_PAGE_TITLE: str = "🍉 24小时等待你的分享，负责整理、体会与反馈。"
    # 用户默认头像
    DEFAULT_AVATAR: str = "prod/default_avatar.png"
    DEFAULT_PROFILE_PIC: str = "prod/default_profile_picture.png"
    # API 版本前缀
    API_V1_STR: str = "/api/v1"
    # 密钥
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 访问令牌过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    # 域名
    DOMAIN: str = "localhost"

    # 环境
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # 普通用户日token上限
    DAILY_TOKEN_LIMIT: int = 12999
    INVITE_CODE_INPUT_REWARD: int = 2999
    INVITE_CODE_SHARE_REWARD: int = 3999

    # @computed_field  # type: ignore[misc]
    # @property
    # def server_host(self) -> str:
    #     # 除了本地开发外，都使用 HTTPS
    #     if self.ENVIRONMENT == "local":
    #         return f"http://{self.DOMAIN}"
    #     return f"https://{self.DOMAIN}"

    # 允许的跨域来源
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # 阿里云密钥
    # ALIBABA_CLOUD_ACCESS_KEY_ID: str
    # ALIBABA_CLOUD_ACCESS_KEY_SECRET: str
    # # 阿里云AI服务gen
    # ALIBABA_DASHSCOPE_API_KEY: str
    # # 阿里云短信服务
    # ALIBABA_SMS_TEMPLATE_CODE: str
    # ALIBABA_SMS_SIGN_NAME: str
    # # 阿里云OSS
    # ALIBABA_OSS_ENDPOINT: str
    # ALIBABA_OSS_BUCKET: str
    # ALIBABA_OSS_FILEPATH: str

    # 项目名称
    PROJECT_NAME: str
    # Sentry DSN
    SENTRY_DSN: HttpUrl | None = None
    # PostgreSQL 服务器
    POSTGRES_SERVER: str
    # PostgreSQL 端口
    POSTGRES_PORT: int = 5432
    # PostgreSQL 用户
    POSTGRES_USER: str
    # PostgreSQL 密码
    POSTGRES_PASSWORD: str
    # PostgreSQL 数据库名称
    POSTGRES_DB: str = ""

    # 数据库连接URL
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        # 构建 PostgreSQL 数据库连接 URI
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # 初始超级用户用户名
    FIRST_SUPERUSER: str
    # 初始超级用户密码
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_PHONE_NUMBER: str
    # # 用户开放注册标志
    # USERS_OPEN_REGISTRATION: bool = True

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        # 检查默认的密钥
        if value == "必须设置":
            message = (
                f' {var_name} 是 "必须设置", '
                "为了安全，必须设置这些值."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        # 强制非默认密钥
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore
