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
from typing import Any
from abc import ABC, abstractmethod
from kubernetes_asyncio import client
from src.generics import AnyRawModel, AnyRawApi


__all__ = ["KupydoBaseModel"]


class KupydoBaseModel(ABC):
    @property
    @abstractmethod
    def raw_api(self) -> AnyRawApi: ...

    @property
    @abstractmethod
    def raw_model(self) -> AnyRawModel: ...

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
