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
from typing import Any
from abc import ABC, abstractmethod
from .types import ApiType, StringDictAtd


__all__ = ["KupydoBaseValues", "KupydoBaseModel"]


class KupydoBaseValues(BaseModel):
    name: str
    labels: StringDictAtd
    annotations: StringDictAtd


class KupydoBaseModel(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    @abstractmethod
    def _api(self) -> ApiType: ...

    @abstractmethod
    def _to_dict(self, new_values: KupydoBaseValues) -> dict: ...

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
