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
from typing import Any, Type
from pydantic import validate_call
from kubernetes_asyncio import client

from models.deployment import Deployment
from models.values.metadata import MetadataValues
from models.abstract import AbstractKubeModel
from typehints import MetaDict


__all__ = ["Namespace"]


class Namespace(AbstractKubeModel):
    Deployment: Type[Deployment] = Deployment

    @validate_call
    def __init__(
            self, *,
            name: str,
            labels: MetaDict = None,
            annotations: MetaDict = None
    ) -> None:
        self.__resources__ = list()
        self.__values__ = MetadataValues(
            name=name,
            labels=labels,
            annotations=annotations
        )

    def __getattribute__(self, item: Any) -> Any:
        def outer(obj2: type) -> callable:
            def inner(*args, **kwargs) -> object:
                obj3 = obj2(*args, **kwargs)
                setattr(obj3, "__namespace__", self.name)
                return obj3
            return inner

        obj = vars(Namespace).get(item)
        if isinstance(obj, type) and issubclass(obj, AbstractKubeModel):
            return outer(obj)
        return super().__getattribute__(item)

    @property
    def values(self) -> MetadataValues:
        return self.__values__

    @values.setter
    def values(self, values: MetadataValues) -> None:
        self.__values__ = values

    @property
    def data_model(self) -> client.V1Namespace:
        return client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=self.values.name,
                labels=self.values.labels,
                annotations=self.values.annotations
            )
        )

    @property
    def api_model(self) -> Type[client.CoreV1Api]:
        return client.CoreV1Api

    async def create(self, session: client.ApiClient) -> client.V1Namespace:
        return await self.api_model(session).create_namespace(self.data_model)

    async def delete(self, session: client.ApiClient) -> client.V1Status:
        return await self.api_model(session).delete_namespace(self.values.name)

    async def read(self, session: client.ApiClient) -> client.V1Namespace:
        return await self.api_model(session).read_namespace(self.values.name)
