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
from kubernetes_asyncio import client, config
from .response import Response, error_handler
from .base import KupydoBaseModel
from .types import RawModel


__all__ = ["ApiClient"]


class ApiClient:
    def __init__(self, *, autoconfig: bool = False):
        self._autoconfig = autoconfig

    async def __aenter__(self):
        kubeconf = client.Configuration.get_default_copy()
        if self._autoconfig and not kubeconf.host:
            try:
                config.load_incluster_config()
            except config.ConfigException:
                try:
                    await config.load_kube_config()
                except config.ConfigException:
                    raise RuntimeError("Unable to automatically load Kubernetes config.")
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
    async def replace(self, model: KupydoBaseModel, *, new_model: KupydoBaseModel) -> Response[RawModel]:
        """
        :raises None:
        """
        return await model.replace(self._client, new_model)

    @error_handler
    async def patch(self, model: KupydoBaseModel, **kwargs) -> Response[RawModel]:
        """
        :raises None:
        """
        return await model.patch(self._client, kwargs)
