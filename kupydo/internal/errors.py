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
from pathlib import Path
from typing import Literal


__all__ = [
    "KupydoBaseError",
    "DisabledRegistryError",
    "ResourcesMissingError",
    "SecretNotFoundError",
    "KwargNotFoundError",
    "ForbiddenPlaintextError",
    "RepoNotFoundError",
    "InvalidPackageError",
    "AssetNotFoundError",
    "BadStatusFileError",
    "InvalidPathTypeError"
]


class KupydoBaseError(Exception):
    """Base class for all Kupydo errors."""
    pass


class DisabledRegistryError(KupydoBaseError):
    def __init__(self):
        super().__init__("Must enable GlobalRegistry before use!")


class ResourcesMissingError(KupydoBaseError):
    def __init__(self):
        super().__init__("Must load resources before accessing resources!")


class SecretNotFoundError(KupydoBaseError):
    def __init__(self, sec_id: str = None):
        a, b, c = (['any ', 's', '.'] if sec_id is None else ['', '', f" by id: '{sec_id}'"])
        super().__init__("Unable to find {0}secret{1} in registry{2}".format(a, b, c))


class KwargNotFoundError(KupydoBaseError):
    def __init__(self, keyword: str, value: str):
        super().__init__(f"Unable to find kwarg in lines for keyword '{keyword}' and value '{value}'")


class ForbiddenPlaintextError(KupydoBaseError):
    def __init__(self, file_path: Path, line_number: int, secret_value: str):
        super().__init__(f"Forbidden plaintext value '{secret_value}'\n"
                         f"on line {line_number} in file '{file_path.name}'.")


class RepoNotFoundError(KupydoBaseError):
    def __init__(self):
        super().__init__("\nCannot use Kupydo library outside of a git repository.")


class InvalidPackageError(KupydoBaseError):
    def __init__(self):
        super().__init__(
            "\nCannot display package info with invalid package data."
            "\nPlease try to re-install kupydo to resolve this issue."
        )


class AssetNotFoundError(KupydoBaseError):
    def __init__(self, tool: str, opsys: str, arch: str):
        super().__init__(
            f"\nUnable to find compatible '{tool}' assets "
            f"for your OS '{opsys}' and platform '{arch}'."
        )


class BadStatusFileError(KupydoBaseError):
    def __init__(self):
        super().__init__("\nNot allowed to write garbage into the status file!")


class InvalidPathTypeError(KupydoBaseError):
    def __init__(self, path: Path | str, expected: Literal["absolute", "relative"]):
        super().__init__(f"\nPath is not {expected}: {path}")
