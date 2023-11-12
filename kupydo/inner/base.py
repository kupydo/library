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
from abc import ABC, abstractmethod
from typing import Type, Literal, Any
from dotmap import DotMap
from .types import ApiType, StringDictAtd
from .registry import GlobalRegistry


__all__ = ["KupydoBaseValues", "KupydoBaseModel"]


class KupydoBaseValues(BaseModel):
    name: str
    labels: StringDictAtd
    annotations: StringDictAtd


class KupydoBaseModel(ABC):

    @abstractmethod
    def __init__(self,
                 values: dict[str, Any],
                 validator: Type[KupydoBaseValues],
                 model: Type[KupydoBaseModel]
                 ) -> None:
        def init(_self, _values: dict[str, Any], _namespace: str):
            _self._values = DotMap(_values)
            _self._namespace = _namespace

        values.pop('self', None)
        valids = validator(**values)
        dump = valids.model_dump(warnings=False)
        GlobalRegistry.insert(
            name=valids.name,
            model=type(
                'DynamicClass', (model, ),
                {'__init__': init}
            ),
            values=dump
        )
        self._values = DotMap(dump)
        self._namespace = 'default'

    def _merge_values(self,
                      kwargs: dict[str, Any],
                      method: Literal['patch', 'replace'],
                      validator: Type[KupydoBaseValues]
                      ) -> DotMap:
        # TODO: Implement method
        pass

    @property
    @abstractmethod
    def _api(self) -> ApiType: ...

    @property
    @abstractmethod
    def _defaults(self) -> dict: ...

    @abstractmethod
    def _raw_model(self, new_values: DotMap = None) -> dict: ...

    @abstractmethod
    async def create(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def delete(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def read(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def replace(self, session: client.ApiClient, kwargs: dict[str, Any]) -> Any: ...

    @abstractmethod
    async def patch(self, session: client.ApiClient, kwargs: dict[str, Any]) -> Any: ...
