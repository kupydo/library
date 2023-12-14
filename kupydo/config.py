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
from kubernetes_asyncio.client import Configuration
from kubernetes_asyncio.config import (
    load_kube_config_from_dict,
    list_kube_config_contexts,
    load_incluster_config,
    load_kube_config,
    ConfigException
)


__all__ = [
    "Configuration",
    "ConfigException",
    "load_kube_config_from_dict",
    "list_kube_config_contexts",
    "load_incluster_config",
    "load_kube_config",
    "autoload_config"
]


async def autoload_config(raise_errors: bool = True) -> bool:
    default = Configuration.get_default_copy()
    if not default.host:
        try:
            load_incluster_config()
        except ConfigException:
            try:
                await load_kube_config()
            except ConfigException:
                if not raise_errors:
                    return False
                raise RuntimeError("Unable to automatically load Kubernetes config.")
        default = Configuration.get_default_copy()
        if not default.host:
            if not raise_errors:
                return False
            raise RuntimeError("Cannot use Kupydo ApiClient without Kubernetes config.")
    return True
