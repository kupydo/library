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
from kupydo.internal.errors import KupydoBaseError


class InvalidPackageError(KupydoBaseError):
    def __init__(self):
        super().__init__(
            "\nCannot display package info with invalid package data."
            "\nPlease try to re-install kupydo to resolve this issue."
        )


class RepoNotFoundError(KupydoBaseError):
    def __init__(self):
        super().__init__("\nCannot use Kupydo CLI outside of a git repository.")
