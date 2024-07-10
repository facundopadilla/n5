from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from src.core.logger import logger
from src.core.types.models import Model


def get_verbose(model: Model) -> str:
    verbose = getattr(model, "__verbose__", None)
    if not verbose:
        verbose = model.__name__.replace('Model', '')
    return verbose


class RecordNotFound(Exception):
    def __init__(self, query_fields: dict, model: Model):
        logger.warning(f"{get_verbose(model)} not found | Query fields: {query_fields}")
        self.query_fields = query_fields
        self.model = model

    @staticmethod
    def exception_handler(request: Request, exc: "RecordNotFound"):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": f"{get_verbose(exc.model)} not found",
                "query_fields": exc.query_fields,
            },
        )


class MultipleRecordNotFound(Exception):

    def __init__(self, query_fields: dict, motive: Optional[str] = None):
        logger.warning(f"Multiple models are not found | Query fields: {query_fields} | Motive: {motive}")
        self.query_fields = query_fields
        self.motive = motive

    @staticmethod
    def exception_handler(request: Request, exc: "MultipleQueryNotFound"):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exc.motive or "Multiple records are not found",
                "query_fields": exc.query_fields
            }
        )


class CreateRecordError(Exception):
    def __init__(
            self, fields: dict, model: Model, exc: Exception, motive: str | None = None
    ):
        logger.error(
            f"Can't create a {get_verbose(model)} instance | Fields: {fields} | Exception: {exc} | Motive: {motive}"
        )
        self.fields = (fields,)
        self.model = model
        self.exc = exc
        self.motive = motive

    @staticmethod
    def exception_handler(request: Request, exc: "CreateRecordError"):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": f"Can't create a {get_verbose(exc.model)}",
                "fields": exc.fields,
                "motive": exc.motive
                          or "An internal error as occurred, please try again.",
            },
        )


class DatabaseError(Exception):
    def __init__(self, model: Model, exc: Exception, motive: str | None = None):
        logger.error(
            f"Error when try to realize a operation into database | Model: {model} | Exception: {exc} | Motive: {motive}"
        )
        self.model = model
        self.exc = exc
        self.motive = motive

    @staticmethod
    def exception_handler(request: Request, exc: "DatabaseError"):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": exc.motive
                          or "An internal error as occurred, please try again.",
            },
        )


class WrongPasswordError(Exception):

    def __init__(self, motive: str | None = "The password do no match"):
        self.motive = motive

    @staticmethod
    def exception_handler(request: Request, exc: "WrongPasswordError"):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exc.motive
            }
        )


def load_exceptions_handlers(app: FastAPI) -> FastAPI:
    for exc in (
        CreateRecordError,
        RecordNotFound,
        DatabaseError,
        MultipleRecordNotFound,
        WrongPasswordError
    ):
        app.add_exception_handler(exc, exc.exception_handler)

    return app
