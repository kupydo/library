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


__all__ = ["Namespace"]


class Namespace(KupydoBaseModel):
    def __init__(self,
                 *,
                 name: str,
                 labels: OptionalDictStr = None,
                 annotations: OptionalDictStr = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=KupydoBaseValues
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
        v: KupydoBaseValues = new_values or self._values
        return client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=v.name,
                annotations=v.annotations,
                labels=v.labels
            )
        ).to_dict()

    async def create(self, session: client.ApiClient) -> client.V1Namespace:
        return await self._api(session).create_namespace(
            body=self._to_dict()
        )

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self._api(session).delete_namespace(
            name=self._values.name
        )

    async def read(self, session: client.ApiClient) -> client.V1Namespace:
        return await self._api(session).read_namespace(
            name=self._values.name
        )

    async def replace(self, session: client.ApiClient, values_from: Namespace) -> client.V1Namespace:
        merged = utils.deep_merge(self._values, values_from.values, self._exclude, method='replace')
        response = await self._api(session).replace_namespace(
            name=self._values.name,
            body=self._to_dict(merged)
        )
        self._values = merged
        return response

    async def patch(self, session: client.ApiClient, values_from: Namespace) -> client.V1Namespace:
        merged = utils.deep_merge(self._values, values_from.values, self._exclude, method='patch')
        response = await self._api(session).patch_namespace(
            name=self._values.name,
            body=self._to_dict(merged)
        )
        self._values = merged
        return response
