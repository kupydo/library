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
from pydantic import BaseModel
from dotmap import DotMap
from abc import ABC, abstractmethod
from typing import Literal, Type, Any
from .registry import (
    DisabledRegistryError,
    GlobalRegistry
)
from .types import *


__all__ = ["KupydoBaseValues", "KupydoBaseModel"]


class KupydoBaseValues(BaseModel):
    name: str
    namespace: NamespaceAtd
    annotations: StringDictAtd
    labels: StringDictAtd


class KupydoBaseModel(ABC):

    @abstractmethod
    def __init__(self, values: dict[str, Any], validator: Type[KupydoBaseValues]) -> None:
        values.pop('self', None)
        valids = validator(**values)
        dump = valids.model_dump(warnings=False)
        self._values = DotMap(dump, _prevent_method_masking=True)
        try:
            GlobalRegistry.register(
                model=type(self),
                values=dump
            )
        except DisabledRegistryError:
            pass

    # def _defaults(self, validator: Type[KupydoBaseValues]) -> dict:
    #     values = validator(name=self._values.name)
    #     dump = values.model_dump(warnings=False)
    #     return DotMap(dump)

    def _merge_values(self,
                      kwargs: dict[str, Any],
                      method: Literal['patch', 'replace'],
                      validator: Type[KupydoBaseValues]
                      ) -> DotMap:
        # TODO: Implement method
        return DotMap()

    @property
    @abstractmethod
    def _api(self) -> ApiType: ...

    @abstractmethod
    def _raw_model(self, new_values: DotMap = None) -> dict: ...

    @abstractmethod
    async def create(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def delete(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def read(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def replace(self, session: client.ApiClient, values_from: KupydoBaseModel) -> Any: ...

    @abstractmethod
    async def patch(self, session: client.ApiClient, values_from: KupydoBaseModel) -> Any: ...
