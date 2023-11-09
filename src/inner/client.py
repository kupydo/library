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
from typing import Generic, TypeVar, Callable
from dataclasses import dataclass
from kubernetes_asyncio import client
from .base import KupydoBaseModel
from .types import AnyRawModel


T = TypeVar('T', bound=KupydoBaseModel)


@dataclass
class ErrorDetails:
    status: str
    reason: str
    message: str
    details: dict


@dataclass
class Response(Generic[T]):
    code: int
    raw: AnyRawModel | None
    error: ErrorDetails | orjson.JSONDecodeError | None

    def __init__(self, model: AnyRawModel = None, error: client.ApiException = None) -> None:
        self.model = model
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


class ApiClient:
    def __init__(self):
        self.__client__ = client.ApiClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client__.close()

    @staticmethod
    def query_handler(async_method: Callable) -> Callable:
        async def closure(model: T) -> Response[T]:
            try:
                resp = await async_method(model)
                return Response(model=resp)
            except client.ApiException as ex:
                return Response(error=ex)
        return closure

    @query_handler
    async def create(self, model: T) -> Response[T]:
        return await model.create(self.__client__)

    @query_handler
    async def delete(self, model: T) -> Response[T]:
        return await model.delete(self.__client__)

    @query_handler
    async def patch(self, model: T) -> Response[T]:
        return await model.patch(self.__client__)

    @query_handler
    async def read(self, model: T) -> Response[T]:
        return await model.read(self.__client__)

    @query_handler
    async def replace(self, model: T) -> Response[T]:
        return await model.replace(self.__client__)
