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
import sys
import importlib.util as imp
from pathlib import Path
from dotmap import DotMap
from typing import Callable, Type, Any
from .sec_ops import SecretFieldDetails
from .utils import is_path_absolute
from .errors import *


__all__ = [
    "GlobalRegistry",
    "LocalRegistry",
    "DynamicTypeRegistry"
]


_ResourceTemplates = list[tuple[Type, dict[str, Any]]]


class GlobalRegistry:
    _templates: _ResourceTemplates = list()
    _secrets: dict[str, SecretFieldDetails] = dict()
    _enabled: bool = False
    _silent: bool = False

    @staticmethod
    def disabled_check(func: Callable) -> Callable:
        def closure(cls, *args, **kwargs):
            if not cls._enabled and not cls._silent:
                raise DisabledRegistryError
            return func(cls, *args, **kwargs)
        return closure

    @disabled_check
    def __new__(cls, *, namespace: str = 'default') -> LocalRegistry:
        if not cls._templates and not cls._silent:
            raise ResourcesMissingError
        return LocalRegistry(cls._templates, namespace)

    @classmethod
    @disabled_check
    def load_resources(cls, path: Path) -> None:
        if not is_path_absolute(path) and not cls._silent:
            raise InvalidPathTypeError(path, "absolute")
        cls.reset()
        spec = imp.spec_from_file_location(path.stem, path)
        module = imp.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)

    @classmethod
    @disabled_check
    def register_template(cls, model: Type, values: dict[str, Any]) -> None:
        cls._templates.append((model, values))

    @classmethod
    @disabled_check
    def register_secret(cls, sfd: SecretFieldDetails) -> None:
        cls._secrets[sfd.enc_tag] = sfd

    @classmethod
    @disabled_check
    def get_all_secrets(cls) -> list[SecretFieldDetails]:
        if len(cls._secrets) == 0 and not cls._silent:
            raise SecretNotFoundError
        return list(cls._secrets.values())

    @classmethod
    @disabled_check
    def get_secret(cls, secret_id: str) -> SecretFieldDetails:
        if secret_id not in cls._secrets and not cls._silent:
            raise SecretNotFoundError(secret_id)
        return cls._secrets.get(secret_id)

    @classmethod
    @disabled_check
    def reset(cls) -> None:
        cls._templates = list()
        cls._secrets = dict()

    @classmethod
    def set_enabled(cls, state: bool) -> None:
        cls._enabled = state

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled

    @classmethod
    def set_silent(cls, state: bool) -> None:
        cls._silent = state

    @classmethod
    def is_silent(cls) -> bool:
        return cls._silent


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
