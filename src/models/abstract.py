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


__all__ = ["AbstractKubeModel"]


class AbstractKubeModel(ABC):
    @property
    @abstractmethod
    def values(self) -> object:
        pass

    @values.setter
    @abstractmethod
    def values(self, values: object) -> None:
        pass

    @property
    @abstractmethod
    def data_model(self) -> object:
        pass

    @property
    @abstractmethod
    def api_model(self) -> object:
        pass

    @abstractmethod
    async def create(self, session: client.ApiClient) -> Any:
        pass

    @abstractmethod
    async def delete(self, session: client.ApiClient) -> Any:
        pass

    # @abstractmethod
    # async def patch(self, session: client.ApiClient) -> None:
    #     pass

    @abstractmethod
    async def read(self, session: client.ApiClient) -> Any:
        pass

    # @abstractmethod
    # async def replace(self, session: client.ApiClient) -> None:
    #     pass
