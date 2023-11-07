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
from dataclasses import dataclass
from kubernetes_asyncio.client.exceptions import ApiException
from typing import Generic, TypeVar


@dataclass
class ErrorDetails:
    status: str
    reason: str
    message: str
    details: dict


AnyModel = TypeVar("AnyModel")


class Response(Generic[AnyModel]):
    code: int
    contents: AnyModel | None
    error: ErrorDetails | orjson.JSONDecodeError | None

    def __init__(self, contents: AnyModel = None, error: ApiException = None) -> None:
        self.contents = contents
        if not error:
            self.code = 200
            self.error = None
        else:
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
                self.error = ex
