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
from rich.panel import Panel
from rich import print
from typing import Callable
from .response import Response
from .base import KupydoModel


__all__ = ["ApiClient"]


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

    @error_handler
    async def patch(self, model: KupydoModel, **kwargs) -> Response[KupydoModel]:
        """
        :raises None:
        """
        return await model.patch(self.__client__, kwargs)
