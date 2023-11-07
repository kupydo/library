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
from models.abstract import AbstractKubeModel
from kubernetes_asyncio import client


class ConfigMap:
    pass

# class ConfigMap:
#
#     def __init__(
#             self,
#             name: str = None,
#             data: dict[str, str] = None,
#             labels: dict[str, str] = None,
#             annotations: dict[str, str] = None,
#             immutable: bool = False,
#             **kwargs: dict[str, str]
#     ) -> None:
#         pass
#         # if data is None:
#         #     data = dict()
#         # data.update(**kwargs)
#         #
#         # client.V1ConfigMap(
#         #     api_version="v1",
#         #     kind="ConfigMap",
#         #     immutable=immutable,
#         #     metadata=client.V1ObjectMeta(
#         #         name=name or generate_name(),
#         #         labels=labels,
#         #         annotations=annotations,
#         #         namespace=
#         #     ),
#         #     data=data
#         # )
#
