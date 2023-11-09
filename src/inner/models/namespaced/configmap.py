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
from typing import Type
from kubernetes_asyncio import client
from src.inner.registry import Registry
from src.inner.base import KupydoBaseModel


class ConfigMap(KupydoBaseModel):

    def __init__(
            self,
            name: str,
            labels: dict[str, str] = None,
            annotations: dict[str, str] = None,
            data: dict[str, str] = None,
            **kwargs
    ) -> None:
        reg = Registry()
        reg.append(self)

    @property
    def raw_api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    @property
    def raw_model(self) -> Type[client.V1ConfigMap]:
        return client.V1ConfigMap

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.raw_api(session).create_namespaced_config_map()

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self.raw_api(session).delete_namespaced_config_map()

    async def patch(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.raw_api(session).patch_namespaced_config_map()

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.raw_api(session).read_namespaced_config_map()

    async def replace(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.raw_api(session).replace_namespaced_config_map()
