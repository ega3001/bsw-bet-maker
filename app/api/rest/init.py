from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .middleware import add_middlewares
from .routes import BetsRouter, MatchesRouter
from core.config import AppConfig


def Init() -> FastAPI:
    if AppConfig.debug:
        app = FastAPI(title="Bet", version="1.0.0")
    else:
        app = FastAPI(title="Bet", version="1.0.0", docs_url=None, redoc_url=None)

    app.include_router(router=MatchesRouter)
    app.include_router(router=BetsRouter)

    add_middlewares(app=app)

    @app.exception_handler(exc_class_or_status_code=RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=({"detail": str(exc.errors()[0]["msg"])}),
        )

    return app
