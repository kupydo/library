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
from typing import Any
from pydantic import BaseModel
from kubernetes_asyncio import client
from .types import *


__all__ = ["KupydoBaseModel"]


class KupydoBaseModel(BaseModel, ABC):
    name: str
    namespace: str = None
    annotations: OptDict = None
    labels: OptDict = None

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
