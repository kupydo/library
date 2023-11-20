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
from __future__ import annotations
from kubernetes_asyncio import client
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Type, Any
from abc import ABC, abstractmethod
from dotmap import DotMap
from kupydo.internal import utils
from .registry import GlobalRegistry
from .errors import DisabledRegistryError
from .types import *


__all__ = [
    "KupydoApiActions",
    "KupydoBaseValues",
    "KupydoBaseModel",
    "KupydoNamespacedModel",
    "KupydoClusterWideModel"
]


@dataclass
class KupydoApiActions:
    create: AsyncCallable
    delete: AsyncCallable
    read: AsyncCallable
    replace: AsyncCallable
    patch: AsyncCallable


class KupydoBaseValues(BaseModel):
    name: str
    namespace: OptionalStr
    annotations: OptionalDictStr
    labels: OptionalDictStr


class KupydoBaseModel(ABC):
    _values = DotMap()

    @abstractmethod
    def __init__(self,
                 values: dict[str, Any],
                 validator: Type[KupydoBaseValues]
                 ) -> None:
        filtered_values = {
            k: v for k, v in values.items()
            if k in validator.model_fields
        }
        valids = validator(**filtered_values)
        dump = valids.model_dump(warnings=False)
        self._values = DotMap(dump, _prevent_method_masking=True)
        try:
            GlobalRegistry.register_model_template(type(self), dump)
        except DisabledRegistryError:
            pass

    @property
    def values(self) -> DotMap:
        return self._values.copy()

    @property
    def _exclude(self) -> DotMap:
        return DotMap(name=True, namespace=True)

    @property
    def _namespace(self) -> dict:
        if isinstance(self, KupydoNamespacedModel):
            return dict(namespace=self._values.namespace)
        return dict()

    @abstractmethod
    def _to_dict(self, new_values: DotMap = None) -> dict: ...

    @abstractmethod
    def _api(self, session: client.ApiClient) -> KupydoApiActions: ...

    async def create(self, session: client.ApiClient) -> RawModel:
        return await self._api(session).create(
            body=self._to_dict(),
            **self._namespace
        )

    async def delete(self, session: client.ApiClient) -> RawModel:
        return await self._api(session).delete(
            name=self._values.name,
            **self._namespace
        )

    async def read(self, session: client.ApiClient) -> RawModel:
        return await self._api(session).read(
            name=self._values.name,
            **self._namespace
        )

    async def replace(self, session: client.ApiClient, values_from: KupydoBaseModel) -> RawModel:
        merged = utils.deep_merge(self._values, values_from.values, self._exclude, method='replace')
        response = await self._api(session).replace(
            name=self._values.name,
            body=self._to_dict(merged),
            **self._namespace
        )
        self._values = merged
        return response

    async def patch(self, session: client.ApiClient, values_from: KupydoBaseModel) -> RawModel:
        merged = utils.deep_merge(self._values, values_from.values, self._exclude, method='patch')
        response = await self._api(session).patch(
            name=self._values.name,
            body=self._to_dict(merged),
            **self._namespace
        )
        self._values = merged
        return response


class KupydoNamespacedModel(KupydoBaseModel, ABC):
    pass


class KupydoClusterWideModel(KupydoBaseModel, ABC):
    pass
