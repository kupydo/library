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
from typing import Type, Any
from dotmap import DotMap
from pathlib import Path


__all__ = [
    "DisabledRegistryError",
    "GlobalRegistry",
    "LocalRegistry",
    "DynamicTypeRegistry"
]


_ResourceTemplates = list[tuple[Type, dict[str, Any]]]


class DisabledRegistryError(Exception):
    def __init__(self):
        super().__init__("Must enable GlobalRegistry before use!")


class GlobalRegistry:
    _templates: _ResourceTemplates = list()
    _enabled: bool = False

    def __new__(cls, *, namespace: str = 'default') -> LocalRegistry:
        if not cls._enabled:
            raise DisabledRegistryError
        return LocalRegistry(cls._templates, namespace)

    @classmethod
    def register(cls, model: Type, values: dict[str, Any]) -> None:
        if not cls._enabled:
            raise DisabledRegistryError
        cls._templates.append((model, values))

    @classmethod
    def load_resources(cls, path: Path) -> None:
        if not cls._enabled:
            raise DisabledRegistryError
        cls.clear_resources()
        #  TODO: import modules with importlib

    @classmethod
    def clear_resources(cls) -> None:
        if not cls._enabled:
            raise DisabledRegistryError
        cls._templates = list()

    @classmethod
    def enable(cls):
        cls._enabled = True

    @classmethod
    def disable(cls):
        cls._enabled = False


class LocalRegistry(list):
    def __init__(self, templates: _ResourceTemplates, namespace: str) -> None:
        super().__init__()
        for [model, values] in templates:
            dynamic = DynamicTypeRegistry.get(model)
            dm_vals = DotMap(values, _prevent_method_masking=True)
            dm_vals.namespace = namespace
            obj = dynamic(dm_vals)
            self.append(obj)


class DynamicTypeRegistry:
    _dynamic_types: dict[str, Type] = dict()

    @staticmethod
    def _init(self, values: DotMap):
        self._values = values

    @classmethod
    def get(cls, model: Type) -> Type:
        name = model.__name__.lower()
        if name not in cls._dynamic_types:
            cls._dynamic_types[name] = type(
                f'Dynamic{model.__name__}Model',
                (model, ), {'__init__': cls._init}
            )
        return cls._dynamic_types[name]
