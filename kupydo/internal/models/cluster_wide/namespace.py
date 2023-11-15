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
from __future__ import annotations as anno
from dotmap import DotMap
from kubernetes_asyncio import client
from kupydo.internal.types import *
from kupydo.internal.base import *


__all__ = ["Namespace"]


class Namespace(KupydoClusterWideModel):
    def __init__(self,
                 *,
                 name: str,
                 labels: OptionalDictStr = None,
                 annotations: OptionalDictStr = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=KupydoBaseValues
        )

    def _to_dict(self, new_values: DotMap = None) -> dict:
        v: KupydoBaseValues = new_values or self._values
        return client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=v.name,
                annotations=v.annotations,
                labels=v.labels
            )
        ).to_dict()

    def _api(self, session: client.ApiClient) -> KupydoApiActions:
        api = client.CoreV1Api(session)
        return KupydoApiActions(
            create=api.create_namespace,
            delete=api.delete_namespace,
            read=api.read_namespace,
            replace=api.replace_namespace,
            patch=api.patch_namespace
        )
