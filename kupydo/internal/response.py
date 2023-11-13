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
from typing import Callable, Generic, Any
from kubernetes_asyncio.client import ApiException
from aiohttp.client import ClientError
from dataclasses import dataclass
from functools import partial
from rich.panel import Panel
from rich import print
from .base import KupydoBaseModel
from .types import RawModel
import utils


__all__ = ["ErrorDetails", "Response", "error_handler"]


@dataclass
class ErrorDetails:
    status: str
    reason: str
    message: str
    details: dict[str, Any] = None


@dataclass
class Response(Generic[RawModel]):
    code: int
    raw: RawModel = None
    error: ErrorDetails = None


def error_handler(coro: Callable) -> Callable:
    async def closure(_self, model: KupydoBaseModel, **kwargs) -> Response[RawModel]:
        try:
            c = partial(coro, _self, model)
            raw = await c(**kwargs) if kwargs else await c()
            return Response(code=200, raw=raw)
        except (ApiException, ClientError, Exception) as error:
            if isinstance(error, ApiException):
                code = int(error.status)
                try:
                    body = orjson.loads(error.body)
                    error = ErrorDetails(
                        status=body.get("status", ""),
                        reason=body.get("reason", ""),
                        message=body.get("message", ""),
                        details=body.get("details", None)
                    )
                except orjson.JSONDecodeError as ex:
                    error = ErrorDetails(
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
            elif isinstance(error, ClientError):
                code = 400
                error = ErrorDetails(
                    status="AiohttpError",
                    reason=error.__class__.__name__,
                    message=str(error)
                )
            else:  # Exception instance
                tb = error.__traceback__
                code = 600
                error = ErrorDetails(
                    status="KupydoError",
                    reason=error.__class__.__name__,
                    message=str(error),
                    details=dict(
                        filename=utils.extract_tb_filepath(tb),
                        instruction=utils.extract_tb_line(tb),
                        lineno=tb.tb_lineno
                    )
                )
            # Always log errors
            err_str = orjson.dumps(
                dict(error=vars(error)),
                option=orjson.OPT_INDENT_2
            )
            panel = Panel(
                renderable=err_str.decode("utf-8"),
                title="Response Error",
                title_align="center",
                expand=False
            )
            print(panel)
            return Response(code=code, error=error)
    return closure
