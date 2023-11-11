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
from kupydo.inner.types import StringDictAtd
from kupydo.inner.base import (
    KupydoBaseValues,
    KupydoBaseModel
)


class ConfigMapValues(KupydoBaseValues):
    immutable: bool
    data: StringDictAtd


class ConfigMap(KupydoBaseModel):
    def __init__(self,
                 *,
                 name: str,
                 labels: StringDictAtd = None,
                 annotations: StringDictAtd = None,
                 data: StringDictAtd = None,
                 immutable: bool = False
                 ) -> None:
        loc = locals()
        loc.pop('self', None)
        self._values = ConfigMapValues(**loc)
        values_dict = self._values.model_dump(warnings=False)
        GlobalRegistry.insert((ConfigMap, values_dict))
        self._namespace = 'default'

    @property
    def _api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    def _to_dict(self, new_values: ConfigMapValues = None) -> dict:
        values = new_values or self._values
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=values.name,
                labels=values.labels,
                annotations=values.annotations,
                namespace=self._namespace
            ),
            immutable=values.immutable,
            data=values.data
        ).to_dict()

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self._api(session).create_namespaced_config_map(
            namespace=self._namespace,
            body=self._to_dict()
        )

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self._api(session).delete_namespaced_config_map(
            name=self._values.name,
            namespace=self._namespace
        )

    async def read(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self._api(session).read_namespaced_config_map(
            name=self._values.name,
            namespace=self._namespace
        )

    async def replace(self, session: client.ApiClient, new_model: ConfigMap) -> client.V1ConfigMap:
        return await self._api(session).replace_namespaced_config_map(
            name=self._values.name,
            namespace=self._namespace,
            body=new_model._to_dict()
        )

    async def patch(self, session: client.ApiClient, kwargs: dict[str, Any]) -> client.V1ConfigMap:
        new_values = ConfigMapValues(**kwargs)
        new_values.name = self._values.name

        response = await self._api(session).patch_namespaced_config_map(
            name=self._values.name,
            namespace=self._namespace,
            body=self._to_dict(new_values)
        )
        self._values = new_values
        return response
