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
from dotmap import DotMap
from src.inner.base import KupydoBaseModel


class GlobalRegistry:
    __private__: {
        "namespace": str
    }
    __namespace__: str | None = None
    __instance__: GlobalRegistry | None = None
    __items__: list[KupydoBaseModel] | None = None

    @classmethod
    def __new__(cls, *_) -> GlobalRegistry:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__namespace__ = None
        return cls.__instance__

    def register(self, model: KupydoBaseModel, *, with_namespace: bool) -> None:
        pass
