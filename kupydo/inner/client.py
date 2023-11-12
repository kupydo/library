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
from .config import autoload_config
from .base import KupydoBaseModel
from .types import RawModel


__all__ = ["ApiClient"]


class ApiClient:
    def __init__(self, *, autoconfig: bool = True) -> None:
        """
        :param autoconfig: When set to True, Kupydo will first try to load the
            in-cluster config. If unsuccessful, it tries to load the current
            context config. When set to False, the user is responsible for
            loading the correct custom config using the `kupydo.config` module.
        :raises RuntimeError: Only on `'async with'`, if Kupydo has not been
            configured manually or is unable to automatically configure itself
            when autoconfig is set to True.
        """
        self._autoconfig = autoconfig

    async def __aenter__(self):
        if self._autoconfig:
            await autoload_config()
        self._client = client.ApiClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.close()

    @error_handler
    async def create(self, model: KupydoBaseModel) -> Response[RawModel]:
        """
        :raises None:
        """
        return await model.create(self._client)

    @error_handler
    async def delete(self, model: KupydoBaseModel) -> Response[RawModel]:
        """
        :raises None:
        """
        return await model.delete(self._client)

    @error_handler
    async def read(self, model: KupydoBaseModel) -> Response[RawModel]:
        """
        :raises None:
        """
        return await model.read(self._client)

    @error_handler
    async def replace(self, model: KupydoBaseModel, **kwargs) -> Response[RawModel]:
        """
        :raises pydantic.ValidationError:
        """
        return await model.replace(self._client, kwargs)

    @error_handler
    async def patch(self, model: KupydoBaseModel, **kwargs) -> Response[RawModel]:
        """
        :raises pydantic.ValidationError:
        """
        return await model.patch(self._client, kwargs)
