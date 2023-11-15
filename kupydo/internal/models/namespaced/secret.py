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


class SecretValues(KupydoBaseValues):
    string_data: OptionalDictStr
    immutable: OptionalBool
    subtype: OptionalStr


class Secret(KupydoNamespacedModel):
    def __init__(self,
                 *,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 subtype: OptionalStr = None,
                 string_data: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=SecretValues
        )

    def _to_dict(self, new_values: DotMap = None) -> dict:
        v: SecretValues = new_values or self._values
        return client.V1Secret(
            api_version="v1",
            kind="Secret",
            metadata=client.V1ObjectMeta(
                name=v.name,
                namespace=v.namespace,
                annotations=v.annotations,
                labels=v.labels
            ),
            string_data=v.string_data,
            immutable=v.immutable,
            type=v.subtype
        ).to_dict()

    def _api(self, session: client.ApiClient) -> KupydoApiActions:
        api = client.CoreV1Api(session)
        return KupydoApiActions(
            create=api.create_namespaced_secret,
            delete=api.delete_namespaced_secret,
            read=api.read_namespaced_secret,
            replace=api.replace_namespaced_secret,
            patch=api.patch_namespaced_secret
        )
