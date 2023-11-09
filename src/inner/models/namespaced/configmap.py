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
from dotmap import DotMap
from kubernetes_asyncio import client
from src.inner.registry import GlobalRegistry
from src.inner.types import StringDict
from src.inner.base import (
    KupydoBaseValues,
    KupydoBaseModel
)


class ConfigMapValues(KupydoBaseValues):
    data: StringDict


class ConfigMap(KupydoBaseModel):
    def __init__(
            self,
            *,
            name: str,
            labels: StringDict = None,
            annotations: StringDict = None,
            data: StringDict = None,
            **kwargs
    ) -> None:
        if data is None:
            data = dict()
        data.update(kwargs)
        lcl = locals()
        [lcl.pop(x) for x in {'self', 'kwargs'}]
        values: ConfigMapValues = DotMap(lcl)
        print(values)

    @property
    def raw(self) -> client.V1ConfigMap:
        return client.V1ConfigMap()

    @property
    def api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    @property
    def values(self) -> None:
        return None

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).create_namespaced_config_map()

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self.api(session).delete_namespaced_config_map()

    async def patch(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).patch_namespaced_config_map()

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).read_namespaced_config_map()

    async def replace(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).replace_namespaced_config_map()
