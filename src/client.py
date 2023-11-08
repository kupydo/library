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
from src.generics import KupydoModel
from src.response import Response


class ApiClient:
    def __init__(self):
        self.__client__ = client.ApiClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client__.close()

    @staticmethod
    def query_handler(async_method: Callable) -> Callable:
        async def closure(model: KupydoModel) -> Response[KupydoModel]:
            try:
                resp = await async_method(model)
                return Response(model=resp)
            except client.ApiException as ex:
                return Response(error=ex)
        return closure

    @query_handler
    async def create(self, model: KupydoModel) -> Response[KupydoModel]:
        return await model.create(self.__client__)

    @query_handler
    async def delete(self, model: KupydoModel) -> Response[KupydoModel]:
        return await model.delete(self.__client__)

    @query_handler
    async def patch(self, model: KupydoModel) -> Response[KupydoModel]:
        return await model.patch(self.__client__)

    @query_handler
    async def read(self, model: KupydoModel) -> Response[KupydoModel]:
        return await model.read(self.__client__)

    @query_handler
    async def replace(self, model: KupydoModel) -> Response[KupydoModel]:
        return await model.replace(self.__client__)
