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
from abc import ABC, abstractmethod
from typing import Any, TypeVar
from pydantic import BaseModel
from kubernetes_asyncio import client
from .types import *


__all__ = [
    "KupydoBaseValues", "KupydoValues",
    "KupydoBaseModel", "KupydoModel"
]


class KupydoBaseValues(BaseModel):
    name: str
    labels: StringDict
    annotations: StringDict


KupydoValues = TypeVar('KupydoValues', bound=KupydoBaseValues)


class KupydoBaseModel(ABC):
    @property
    @abstractmethod
    def raw(self) -> RawModel: ...

    @property
    @abstractmethod
    def api(self) -> ApiType: ...

    @property
    @abstractmethod
    def values(self) -> KupydoBaseValues: ...

    @abstractmethod
    async def create(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def delete(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def patch(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def read(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def replace(self, session: client.ApiClient) -> Any: ...


KupydoModel = TypeVar('KupydoModel', bound=KupydoBaseModel)
