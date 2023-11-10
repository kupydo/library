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
from typing import Any, TypeVar
from abc import ABC, abstractmethod
from .types import ApiType, StringDict


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
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    @abstractmethod
    def __api__(self) -> ApiType: ...

    @abstractmethod
    def to_dict(self, new_values: KupydoBaseValues) -> dict | None: ...

    @abstractmethod
    async def create(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def delete(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def read(self, session: client.ApiClient) -> Any: ...

    @abstractmethod
    async def replace(self, session: client.ApiClient, new_model: KupydoBaseModel) -> Any: ...

    @abstractmethod
    async def patch(self, session: client.ApiClient, kwargs: dict[str, Any]) -> Any: ...


KupydoModel = TypeVar('KupydoModel', bound=KupydoBaseModel)
