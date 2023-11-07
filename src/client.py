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
from typing import Callable
from kubernetes_asyncio import client
from typehints import KubeModel
from response import Response


class ApiClient:
    def __init__(self):
        self.__client__ = client.ApiClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client__.close()
        self.__client__ = None

    async def _request(self, coro: Callable) -> Response:
        try:
            resp = await coro(self.__client__)
            return Response(contents=resp)
        except client.ApiException as ex:
            return Response(error=ex)

    async def create(self, model: KubeModel) -> Response:
        return await self._request(model.create)

    async def delete(self, model: KubeModel) -> Response:
        return await self._request(model.delete)

    async def read(self, model: KubeModel) -> Response:
        return await self._request(model.read)
