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
from typing import TypeVar
from kubernetes_asyncio import client
from src.base import KupydoBaseModel


__all__ = ["KupydoModel", "AnyRawApi", "AnyRawModel"]


KupydoModel = TypeVar(
    name='KupydoModel',
    bound=KupydoBaseModel
)
AnyRawApi = TypeVar(
    'AnyRawApi',
    client.AppsV1Api,
    client.AutoscalingV1Api,
    client.CoreV1Api,
    client.BatchV1Api,
    client.NetworkingV1Api,
    client.RbacAuthorizationV1Api,
    client.PolicyV1Api
)
AnyRawModel = TypeVar(
    'AnyRawModel',
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
