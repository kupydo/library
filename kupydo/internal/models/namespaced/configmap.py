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
from kupydo.internal.types import *
from kupydo.internal.base import *
from kupydo.internal import utils


class ConfigMapValues(KupydoBaseValues):
    data: OptionalDictStr
    immutable: OptionalBool


class ConfigMap(KupydoBaseModel):
    def __init__(self,
                 *,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 data: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=ConfigMapValues
        )

    @property
    def _api(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    @property
    def _exclude(self) -> DotMap:
        return DotMap(
            name=True,
            namespace=True
        )

    def _to_dict(self, new_values: DotMap = None) -> dict:
        v: ConfigMapValues = new_values or self._values
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=v.name,
                namespace=v.namespace,
                annotations=v.annotations,
                labels=v.labels
            ),
            immutable=v.immutable,
            data=v.data
        ).to_dict()

    async def create(self, session: client.ApiClient) -> client.V1ConfigMap:
        return await self._api(session).create_namespaced_config_map(
            namespace=self._values.namespace,
            body=self._to_dict()
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

    async def replace(self, session: client.ApiClient, new: ConfigMap) -> client.V1ConfigMap:
        merged = utils.deep_merge(self._values, new.values, self._exclude, method='replace')
        response = await self._api(session).replace_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace,
            body=self._to_dict(merged)
        )
        self._values = merged
        return response

    async def patch(self, session: client.ApiClient, new: ConfigMap) -> client.V1ConfigMap:
        merged = utils.deep_merge(self._values, new.values, self._exclude, method='patch')
        response = await self._api(session).patch_namespaced_config_map(
            name=self._values.name,
            namespace=self._values.namespace,
            body=self._to_dict(merged)
        )
        self._values = merged
        return response
