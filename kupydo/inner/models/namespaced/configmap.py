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
from __future__ import annotations as anno
from typing import Type
from dotmap import DotMap
from kubernetes_asyncio import client
from kupydo.inner.registry import GlobalRegistry
from kupydo.inner.types import StringDict
from kupydo.inner.base import (
    KupydoBaseFields,
    KupydoBaseModel
)


class ConfigMapFields(KupydoBaseFields):
    immutable: bool
    data: StringDict


class ConfigMap(KupydoBaseModel):
    def __init__(
            self,
            *,
            name: str,
            data: StringDict = None,
            labels: StringDict = None,
            annotations: StringDict = None,
            immutable: bool = False
    ) -> None:
        lcl = locals()
        lcl.
        lcl.pop('self')
        self.__values__ = DotMap(lcl)

    @property
    def raw(self) -> client.V1ConfigMap:
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=self.values.name,
                labels=self.values.labels,
                annotations=self.values.annotations
            ),
            immutable=self.values.immutable,
            data=dict(self.values.data)
        )

    @property
    def api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    @property
    def values(self) -> ConfigMapFields:
        return self.__values__

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).create_namespaced_config_map(
            namespace=GlobalRegistry.namespace,
            body=self.raw.to_dict()
        )

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self.api(session).delete_namespaced_config_map(
            namespace=GlobalRegistry.namespace,
            name=self.values.name
        )

    async def patch(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).patch_namespaced_config_map(
            namespace=GlobalRegistry.namespace,
            name=self.values.name,
            body=self.raw.to_dict()
        )

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.api(session).read_namespaced_config_map(
            namespace=GlobalRegistry.namespace,
            name=self.values.name
        )

    async def replace(self, session: client.ApiClient, new_model: ConfigMap) -> client.V1ConfigMap:
        return await self.api(session).replace_namespaced_config_map(
            namespace=GlobalRegistry.namespace,
            name=self.values.name,
            body=new_model.raw.to_dict()
        )
