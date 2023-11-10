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
from kubernetes_asyncio import client
from dataclasses import dataclass
from typing import Generic, Any
from .base import KupydoModel
from .types import RawModel
from .utils import pathutils


__all__ = ["ErrorDetails", "Response"]


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
