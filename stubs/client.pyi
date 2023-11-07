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
from typing import overload, Callable
from kubernetes_asyncio import client
from response import Response
from models import *


class ApiClient:
    def __init__(self):
        self.__client__ = ApiClient()

    async def __aenter__(self) -> ApiClient: ...

    async def _request(self, coro: Callable) -> Response: ...

    @overload
    async def create(self, model: Namespace) -> Response[client.V1Namespace]: ...
    @overload
    async def create(self, model: ConfigMap) -> Response[client.V1ConfigMap]: ...
    @overload
    async def create(self, model: Secret) -> Response[client.V1Secret]: ...
    @overload
    async def create(self, model: Deployment) -> Response[client.V1Deployment]: ...

    @overload
    async def delete(self, model: Namespace) -> Response[client.V1Status]: ...
    @overload
    async def delete(self, model: ConfigMap) -> Response[client.V1Status]: ...
    @overload
    async def delete(self, model: Secret) -> Response[client.V1Status]: ...
    @overload
    async def delete(self, model: Deployment) -> Response[client.V1Status]: ...

    @overload
    async def read(self, model: Namespace) -> Response[client.V1Namespace]: ...
    @overload
    async def read(self, model: ConfigMap) -> Response[client.V1ConfigMap]: ...
    @overload
    async def read(self, model: Secret) -> Response[client.V1Secret]: ...
    @overload
    async def read(self, model: Deployment) -> Response[client.V1Deployment]: ...
