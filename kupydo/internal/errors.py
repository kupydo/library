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
__all__ = [
    "KupydoBaseError",
    "DisabledRegistryError",
    "ResourcesMissingError",
    "SecretNotFoundError"
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
    def __init__(self, enc_id: str):
        super().__init__(f"Unable to find secret in registry by id: '{enc_id}'")
