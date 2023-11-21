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
from dataclasses import dataclass
from typing import Callable, Type, Any
from dotmap import DotMap
from pathlib import Path
from kupydo.internal.errors import *


__all__ = [
    "SecretFieldDetails",
    "GlobalRegistry",
    "LocalRegistry",
    "DynamicTypeRegistry"
]


_ResourceTemplates = list[tuple[Type, dict[str, Any]]]


@dataclass
class SecretFieldDetails:
    file_path: Path
    line_number: int
    field_key: str
    field_value: str
    secret_value: str


class GlobalRegistry:
    _templates: _ResourceTemplates = list()
    _plaintext: list[SecretFieldDetails] = list()
    _decrypted: dict[str, str] = dict()
    _enabled: bool = False

    @staticmethod
    def disabled_check(func: Callable) -> Callable:
        def closure(cls, *args, **kwargs):
            if not cls._enabled:
                raise DisabledRegistryError
            return func(cls, *args, **kwargs)
        return closure

    @disabled_check
    def __new__(cls, *, namespace: str = 'default') -> LocalRegistry:
        if not cls._templates:
            raise ResourcesMissingError
        return LocalRegistry(cls._templates, namespace)

    @classmethod
    @disabled_check
    def load_resources(cls, path: Path) -> None:
        cls.reset()
        print(path)
        #  TODO: import modules with importlib

    @classmethod
    @disabled_check
    def register_model_template(cls, model: Type, values: dict[str, Any]) -> None:
        cls._templates.append((model, values))

    @classmethod
    @disabled_check
    def register_plaintext_secret(cls, sfd: SecretFieldDetails) -> None:
        cls._plaintext.append(sfd)

    @classmethod
    @disabled_check
    def register_decrypted_secret(cls, secret_id: str, value: str) -> None:
        cls._decrypted[secret_id] = value

    @classmethod
    @disabled_check
    def get_all_plaintext_secrets(cls) -> list[SecretFieldDetails]:
        if len(cls._plaintext) == 0:
            raise SecretNotFoundError
        return cls._plaintext

    @classmethod
    @disabled_check
    def pop_decrypted_secret(cls, secret_id: str) -> str:
        if secret_id not in cls._decrypted:
            raise SecretNotFoundError(secret_id)
        return cls._decrypted.pop(secret_id)

    @classmethod
    @disabled_check
    def reset(cls) -> None:
        cls._templates = list()
        cls._plaintext = list()
        cls._decrypted = dict()

    @classmethod
    def set_enabled(cls, *, state: bool) -> None:
        cls._enabled = state

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled


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
