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
from kubernetes_asyncio import client
from .response import Response, error_handler
from .configs import autoload_config
from .base import KupydoBaseModel
from .types import RawModel


__all__ = ["ApiClient"]


class ApiClient:
    def __init__(self, *, autoconfig: bool = True) -> None:
        self._autoconfig = autoconfig

    async def __aenter__(self):
        if self._autoconfig:
            await autoload_config()
        self._client = client.ApiClient()
        return self

    async def __aexit__(self, *_):
        await self._client.close()

    @error_handler
    async def create(self, model: KupydoBaseModel) -> Response[RawModel]:
        return await model.create(self._client)

    @error_handler
    async def delete(self, model: KupydoBaseModel) -> Response[RawModel]:
        return await model.delete(self._client)

    @error_handler
    async def read(self, model: KupydoBaseModel) -> Response[RawModel]:
        return await model.read(self._client)

    @error_handler
    async def replace(self, model: KupydoBaseModel, values_from: KupydoBaseModel) -> Response[RawModel]:
        return await model.replace(self._client, values_from)

    @error_handler
    async def patch(self, model: KupydoBaseModel, values_from: KupydoBaseModel) -> Response[RawModel]:
        return await model.patch(self._client, values_from)
