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
from pathlib import Path
from typing import Any


__all__ = ["GlobalRegistry", "LocalRegistry"]


_Entry = tuple[type, dict[str, Any]]
_Registry = dict[str, _Entry]


class GlobalRegistry:
    _registry: _Registry = dict()

    def __new__(cls, *, namespace: str = 'default') -> LocalRegistry:
        return LocalRegistry(cls._registry, namespace)

    @classmethod
    def insert(cls, name: str, model: type, values: dict[str, Any]) -> None:
        cls._registry[name] = (model, values)

    @classmethod
    def clear(cls) -> None:
        cls._registry = dict()

    @classmethod
    def pop(cls, key: str) -> None:
        return cls._registry.pop(key, None)

    @classmethod
    def load_resources(cls, path: Path) -> None:
        cls.clear()
        #  TODO: import modules with importlib


class LocalRegistry(dict):
    def __init__(self, registry: _Registry, namespace: str) -> None:
        for name, [model, values] in registry.items():
            self[name] = model(values, namespace)
        super().__init__()
