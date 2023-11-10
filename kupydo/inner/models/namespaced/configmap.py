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
from typing import Type, Any
from kubernetes_asyncio import client
from kupydo.inner.registry import GlobalRegistry
from kupydo.inner.types import StringDict
from kupydo.inner.base import (
    KupydoBaseValues,
    KupydoBaseModel
)


class ConfigMapValues(KupydoBaseValues):
    immutable: bool
    data: StringDict


class ConfigMap(KupydoBaseModel):
    def __init__(self,
                 *,
                 name: str,
                 labels: StringDict = None,
                 annotations: StringDict = None,
                 data: StringDict = None,
                 immutable: bool = False
                 ) -> None:
        loc = locals()
        loc.pop('self', None)
        self.__values__ = ConfigMapValues(**loc)
        GlobalRegistry().insert(self)

    @property
    def __api__(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    def to_dict(self, new_values: ConfigMapValues = None) -> dict | None:
        if new_values and not isinstance(new_values, ConfigMapValues):
            return None
        values = new_values or self.__values__
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=values.name,
                labels=values.labels,
                annotations=values.annotations,
                namespace=GlobalRegistry().namespace
            ),
            immutable=values.immutable,
            data=values.data
        ).to_dict()

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.__api__(session).create_namespaced_config_map(
            namespace=GlobalRegistry().namespace,
            body=self.to_dict()
        )

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self.__api__(session).delete_namespaced_config_map(
            namespace=GlobalRegistry().namespace,
            name=self.__values__.name
        )

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self.__api__(session).read_namespaced_config_map(
            namespace=GlobalRegistry().namespace,
            name=self.__values__.name
        )

    async def replace(self, session: client.ApiClient, new_model: ConfigMap) -> client.V1ConfigMap:
        return await self.__api__(session).replace_namespaced_config_map(
            namespace=GlobalRegistry().namespace,
            name=self.__values__.name,
            body=new_model.to_dict()
        )

    async def patch(self, session: client.ApiClient, kwargs: dict[str, Any]) -> client.V1ConfigMap:
        new_values = ConfigMapValues(**kwargs)
        new_values.name = self.__values__.name

        response = await self.__api__(session).patch_namespaced_config_map(
            namespace=GlobalRegistry().namespace,
            name=self.__values__.name,
            body=self.to_dict(new_values)
        )
        self.__values__ = new_values
        return response
