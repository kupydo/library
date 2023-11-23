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
import uuid


__all__ = [
    "generate_sid",
    "get_sid_delimiters",
    "validate_sid",
    "wrap_sid",
    "unwrap_sid",
    "sanitize_wrapped_sid"
]


def generate_sid() -> str:
    return uuid.uuid4().hex


def get_sid_delimiters() -> tuple[str, str]:
    return "[ENC_ID>", "<ID_END]"


def validate_sid(sid: str, check_delimiters: bool = True) -> str | None:
    if check_delimiters:
        prefix, suffix, = get_sid_delimiters()
        if not sid.startswith(prefix):
            return None
        elif not sid.endswith(suffix):
            return None
        sid = sid.lstrip(prefix).rstrip(suffix)

    if not len(sid) == 32:
        return None
    elif not all([c in '0123456789abcdef' for c in sid]):
        return None
    return sid


def wrap_sid(unwrapped_sid: str) -> str | None:
    if validate_sid(unwrapped_sid, check_delimiters=False):
        prefix, suffix = get_sid_delimiters()
        return f"{prefix}{unwrapped_sid}{suffix}"


def unwrap_sid(wrapped_sid: str) -> str | None:
    if unwrapped_sid := validate_sid(wrapped_sid):
        return unwrapped_sid


def sanitize_wrapped_sid(dirty_sid: str) -> str | None:
    start_index = dirty_sid.find('[')
    end_index = dirty_sid.rfind(']')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return dirty_sid[start_index:end_index + 1]
    return None
