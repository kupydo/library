#
#   MIT License
#
#   Copyright (c) 2023, Mattias Aabmets
#
#   The contents of this file are subject to the terms and conditions defined in the License.
#   You may not use, modify, or distribute this file except in compliance with the License.
#
#   SPDX-License-Identifier: MIT
#
import orjson
from rich import print
from rich.panel import Panel
from dataclasses import dataclass
from kubernetes_asyncio import client
from typing import Generic, Callable, Any
from .base import KupydoModel
from .types import RawModel
from .utils import pathutils


__all__ = ["ErrorDetails", "Response", "ApiClient"]


@dataclass
class ErrorDetails:
    status: str
    reason: str
    message: str
    details: dict[str, Any]


@dataclass
class Response(Generic[KupydoModel]):
    code: int
    model: RawModel | None
    error: ErrorDetails | str | None

    def __init__(self, model: RawModel = None, error: client.ApiException | Exception = None) -> None:
        self.model = model
        self.error = error

        if error is None:
            self.code = 200
        elif isinstance(error, client.ApiException):
            self.code = int(error.status)
            try:
                body = orjson.loads(error.body)
                self.error = ErrorDetails(
                    status=body.get("status", ""),
                    reason=body.get("reason", ""),
                    message=body.get("message", ""),
                    details=body.get("details", {})
                )
            except orjson.JSONDecodeError as ex:
                self.error = ErrorDetails(
                    status="InvalidResponse",
                    reason="JSONDecodeError",
                    message=ex.msg,
                    details=dict(
                        pos=ex.pos,
                        colno=ex.colno,
                        lineno=ex.lineno,
                        doc=ex.doc
                    )
                )
        else:  # Exception
            tb = error.__traceback__
            self.code = 600
            self.error = ErrorDetails(
                status="KupydoError",
                reason=error.__class__.__name__,
                message=str(error),
                details=dict(
                    filename=pathutils.extract_tb_filepath(tb),
                    instruction=pathutils.extract_tb_line(tb),
                    lineno=tb.tb_lineno
                )
            )


class ApiClient:
    def __init__(self):
        self.__client__ = client.ApiClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client__.close()

    @staticmethod
    def error_handler(async_method: Callable) -> Callable:
        async def closure(model: KupydoModel) -> Response[KupydoModel]:
            try:
                resp = await async_method(model)
                return Response(model=resp)
            except (client.ApiException, Exception) as ex:
                resp = Response(error=ex)
                if True:
                    err_str = orjson.dumps(
                        dict(error=vars(resp.error)),
                        option=orjson.OPT_INDENT_2
                    )
                    panel = Panel(
                        renderable=err_str.decode("utf-8"),
                        title="Response Error",
                        title_align="center",
                        expand=False
                    )
                    print(panel)
                return resp
        return closure

    @error_handler
    async def create(self, model: KupydoModel) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.create(self.__client__)

    @error_handler
    async def delete(self, model: KupydoModel) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.delete(self.__client__)

    @error_handler
    async def patch(self, model: KupydoModel) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.patch(self.__client__)

    @error_handler
    async def read(self, model: KupydoModel) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.read(self.__client__)

    @error_handler
    async def replace(self, model: KupydoModel, new_model: KupydoModel) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.replace(self.__client__, new_model)
