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
from dotmap import DotMap
from typing import Type, Any
from kubernetes_asyncio import client
from kupydo.internal.types import *
from kupydo.internal.base import (
    KupydoBaseValues,
    KupydoBaseModel
)


class ConfigMapValues(KupydoBaseValues):
    data: StringDictAtd
    immutable: bool = False


class ConfigMap(KupydoBaseModel):
    def __init__(self,
                 *,
                 name: str,
                 namespace: NamespaceAtd = None,
                 annotations: StringDictAtd = None,
                 labels: StringDictAtd = None,
                 data: StringDictAtd = None,
                 immutable: bool = False
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=ConfigMapValues
        )

    @property
    def _api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    def _raw_model(self, new_values: DotMap = None) -> dict:
        v: ConfigMapValues = new_values or self._values
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=v.name,
                labels=v.labels,
                annotations=v.annotations,
                namespace=v.namespace
            ),
            immutable=v.immutable,
            data=v.data
        ).to_dict()

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self._api(session).create_namespaced_config_map(
            namespace=self._values.namespace,
            body=self._raw_model()
        )

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self._api(session).delete_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace
        )

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self._api(session).read_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace
        )

    async def replace(self, session: client.ApiClient, kwargs: dict[str, Any]) -> client.V1ConfigMap:
        merged_values = self._merge_values(kwargs, method='replace', validator=ConfigMapValues)
        response = await self._api(session).replace_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace,
            body=self._raw_model(merged_values)
        )
        self._values = merged_values
        return response

    async def patch(self, session: client.ApiClient, kwargs: dict[str, Any]) -> client.V1ConfigMap:
        merged_values = self._merge_values(kwargs, method='patch', validator=ConfigMapValues)
        response = await self._api(session).patch_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace,
            body=self._raw_model(merged_values)
        )
        self._values = merged_values
        return response
