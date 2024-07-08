

from .api.main import api_router

from app.core.config import settings
from fastapi import FastAPI

# 创建 FastAPI 应用程序实例
app = FastAPI(
    # title=settings.PROJECT_NAME,  # 设置项目名称
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",  # 设置 OpenAPI URL
    # generate_unique_id_function=custom_generate_unique_id,  # 设置生成唯一标识符的函数
    # docs_url=None if settings.ENVIRONMENT == "production" else "/bellybookdoc",  # 禁用 Swagger 文档,
    # redoc_url=None,  # 禁用 Redoc 文档,
)


# 添加主 API 路由器，指定前缀为 API_V1_STR
app.include_router(api_router, prefix=settings.API_V1_STR)
