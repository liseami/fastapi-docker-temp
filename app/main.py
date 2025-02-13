"""FastAPI应用入口。

负责:
- FastAPI应用实例配置
- 路由和中间件注册
- 应用生命周期管理
- API文档配置

用法:
    uvicorn main:app --reload
"""


import logging
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from app.models.public_models.Out import ErrorMod
from .api.main import api_router
from app.core.config import settings
from fastapi import FastAPI, Request

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#       _                      _
#   ___| |__  _   _ _ __ __  _(_) __ _ _ __   __ _
#  / __| '_ \| | | | '_ \\ \/ / |/ _` | '_ \ / _` |
# | (__| | | | |_| | | | |>  <| | (_| | | | | (_| |
#  \___|_| |_|\__,_|_| |_/_/\_\_|\__,_|_| |_|\__, |
#                                            |___/
#   __           _              _   _
#  / _| __ _ ___| |_ __ _ _ __ (_) | |_ ___ _ __ ___  _ __
# | |_ / _` / __| __/ _` | '_ \| | | __/ _ \ '_ ` _ \| '_ \
# |  _| (_| \__ \ || (_| | |_) | | | ||  __/ | | | | | |_) |
# |_|  \__,_|___/\__\__,_| .__/|_|  \__\___|_| |_| |_| .__/
#                        |_|                         |_|

@asynccontextmanager
async def lifespan(app: FastAPI):
    """管理应用生命周期。

    记录启动和关闭事件的关键信息。

    参数:
        app: FastAPI应用实例
    """
    # 启动日志
    logger.info("""
#>  ___________________________________
#> / 纯想: 纯想fastapi模版    \\
#> | 在2025年新年之际为0基础全栈开发课程搭建  |
#> | 方便你快速启动一个fastapi后端项目的开发  |
#> | https://chunxiang.space             |
#> |                                     |
#> \\ 2025                               /
#>  ------------------------------------
#>          \\
#>           \\
#> 
#>             |\\___/|
#>           ==) ^Y^ (==
#>             \\  ^  /
#>              )=*=(
#>             /     \\
#>             |     |
#>            /| | | |\\
#>            \\| | |_|/\\
#>       zcx  //_// ___/
#>                \\_)
    """)
    logger.info("🚀 —————————————————— 程序启动")
    logger.info(f"🌍 运行环境: {settings.ENVIRONMENT}")
    logger.info(f"📝 项目名称: {settings.PROJECT_NAME}")
    logger.info(f"🔗 API路径: {settings.API_V1_STR}")
    logger.info("✅ —————————————————— 程序启动")

    yield

    # 关闭日志
    logger.info("👋 —————————————————— 程序关闭")


# 初始化FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # 生产环境禁用文档
    # docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    # redoc_url=None,
    lifespan=lifespan,
)


# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(ErrorMod)
async def error_mod_exception_handler(request: Request, exc: ErrorMod):
    """处理自定义错误。

    参数:
        request: 触发异常的请求
        exc: ErrorMod异常实例

    返回:
        包含错误详情的JSON响应
    """
    msg = f"{exc.message}"
    logger.error(f"ErrorMod exception: {msg}")
    return JSONResponse(
        status_code=200,
        content={"message": msg, "code": 500},
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """处理数据库异常。

    参数:
        request: 触发异常的请求
        exc: SQLAlchemy异常实例

    返回:
        通用错误响应
    """
    logger.error(f"Database error for URL {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"message": "Service temporarily unavailable. Please try again later."})
