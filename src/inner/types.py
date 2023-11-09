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
from pydantic import Field
from typing import TypeVar, Type, Annotated, Union
from kubernetes_asyncio import client


__all__ = ["DataTypes", "UnionDict", "StringDict", "ApiType", "RawModel"]


DataTypes = Union[str, int, float, dict, list]
UnionDict = Annotated[dict[str, DataTypes], Field(default=None)]
StringDict = Annotated[dict[str, str], Field(default=None)]

ApiType = TypeVar(
    'ApiType',
    Type[client.AppsV1Api],
    Type[client.AutoscalingV1Api],
    Type[client.CoreV1Api],
    Type[client.BatchV1Api],
    Type[client.NetworkingV1Api],
    Type[client.RbacAuthorizationV1Api],
    Type[client.PolicyV1Api]
)
RawModel = TypeVar(
    'RawModel',
    client.V1ConfigMap,
    client.V1CronJob,
    client.V1Deployment,
    client.V1HorizontalPodAutoscaler,
    client.V1Ingress,
    client.V1Job,
    client.V1NetworkPolicy,
    client.V1PersistentVolumeClaim,
    client.V1Pod,
    client.V1PodDisruptionBudget,
    client.V1Role,
    client.V1RoleBinding,
    client.V1Secret,
    client.V1Service,
    client.V1ServiceAccount
)
