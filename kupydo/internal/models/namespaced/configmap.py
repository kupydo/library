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


class ConfigMapValues(KupydoBaseValues):
    data: OptionalDictStr
    immutable: OptionalBool


class ConfigMap(KupydoNamespacedModel):
    def __init__(self,
                 *,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 data: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=ConfigMapValues
        )

    def _to_dict(self, new_values: DotMap = None) -> dict:
        v: ConfigMapValues = new_values or self._values
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=v.name,
                namespace=v.namespace,
                annotations=v.annotations,
                labels=v.labels
            ),
            immutable=v.immutable,
            data=v.data
        ).to_dict()

    def _api(self, session: client.ApiClient) -> KupydoApiActions:
        api = client.CoreV1Api(session)
        return KupydoApiActions(
            create=api.create_namespaced_config_map,
            delete=api.delete_namespaced_config_map,
            read=api.read_namespaced_config_map,
            replace=api.replace_namespaced_config_map,
            patch=api.patch_namespaced_config_map
        )
