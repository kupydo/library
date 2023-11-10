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
from kupydo.inner.base import KupydoBaseModel


class GlobalRegistry:
    __entries__: list[KupydoBaseModel]
    __instance__: GlobalRegistry
    __namespace__: str

    @classmethod
    def __new__(cls) -> GlobalRegistry:
        if cls.__instance__ is None:
            obj = super().__new__(cls)
            obj.__entries__ = list()
            cls.__instance__ = obj
        return cls.__instance__

    def insert(self, item: KupydoBaseModel) -> None:
        self.__entries__.append(item)

    @property
    def namespace(self) -> str:
        return self.__namespace__
