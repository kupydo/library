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


class Registry(list):
    __instance__: Registry | None = None

    def __new__(cls) -> Registry:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
        return cls.__instance__
