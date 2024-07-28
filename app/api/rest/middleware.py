import logging
import time
from typing import Type

from fastapi import FastAPI, Request, Response, HTTPException
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.config import AppConfig


def accessMiddleware(logger: logging.Logger) -> Type[BaseHTTPMiddleware]:
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
        ) -> Response:
            started_at: float = time.perf_counter()
            response: Response = await call_next(request)
            request_time: float = time.perf_counter() - started_at

            status_code: int = response.status_code

            logger.info(
                f"{request.method}:{request.url} STATUS={status_code} TIME({request_time})"
            )
            return response

    return Middleware


def exceptionHandlerMiddleware(logger: logging.Logger) -> Type[BaseHTTPMiddleware]:
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
        ) -> Response:
            try:
                return await call_next(request)
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.exception(msg=f"Caught unhandled {e.__class__} exception: {e}")
                return Response("Internal Server Error", status_code=500)

    return Middleware


def add_middlewares(app: FastAPI) -> None:
    # do not change order
    # excLogger: logging.Logger = logging.getLogger("app")
    # accLogger: logging.Logger = logging.getLogger("access")
    # app.add_middleware(exceptionHandlerMiddleware(excLogger))
    # app.add_middleware(accessMiddleware(accLogger))
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origin_regex=AppConfig.server.origin,
    #     allow_credentials=True,
    #     allow_methods=["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"],
    #     allow_headers=["Content-Type", "Set-Cookie", "Authorization"],
    # )
    ...
