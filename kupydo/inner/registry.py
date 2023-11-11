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
from __future__ import annotations
from threading import Lock
from pathlib import Path
from dotmap import DotMap
from typing import Type, Any
from .base import KupydoBaseModel


__all__ = [
    "UnpackedResource",
    "DisabledRegistryError",
    "GlobalRegistry",
    "LocalRegistry"
]

UnpackedResource = tuple[Type[KupydoBaseModel], dict[str, Any]]


class DisabledRegistryError(Exception):
    def __init__(self):
        super().__init__("Cannot use GlobalRegistry when it has been disabled.")


class GlobalRegistry:
    _unpacked_resources: list[UnpackedResource] = list()
    _enabled: bool = True

    def __new__(cls, *, namespace: str = 'default') -> LocalRegistry:
        """
        :raises DisabledRegistryError:
        """
        if not cls._enabled:
            raise DisabledRegistryError
        return LocalRegistry(cls._unpacked_resources, namespace)

    @classmethod
    def enable(cls) -> None:
        """
        :raises None:
        """
        cls._enabled = True

    @classmethod
    def disable(cls) -> None:
        """
        :raises None:
        """
        cls._enabled = False

    @classmethod
    def insert(cls, item: UnpackedResource) -> None:
        """
        :raises None:
        """
        if cls._enabled:
            cls._unpacked_resources.append(item)

    @classmethod
    def clear(cls) -> None:
        """
        :raises None:
        """
        if cls._enabled:
            cls._unpacked_resources = list()

    @classmethod
    def load_resources(cls, path: Path) -> None:
        """
        :raises DisabledRegistryError:
        """
        if not cls._enabled:
            raise DisabledRegistryError
        cls.clear()
        #  TODO: import modules with importlib


class LocalRegistry(list[KupydoBaseModel]):
    _lock = Lock()  # class-level lock

    def __init__(self, unpacked_resources: list[UnpackedResource], namespace: str) -> None:
        def init_override(_self, _values):
            _self._namespace = namespace
            _self._values = _values

        resources = list()
        with LocalRegistry._lock:
            for model_class, model_values in unpacked_resources:
                default_init = model_class.__init__
                model_class.__init__ = init_override
                resource = model_class(DotMap(model_values))
                model_class.__init__ = default_init
                resources.append(resource)
        super().__init__(resources)
