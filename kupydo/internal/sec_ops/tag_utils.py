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
    "generate_enc_tag",
    "enc_tag_delimiters",
    "validate_enc_tag",
    "wrap_enc_tag",
    "unwrap_enc_tag",
    "sanitize_wrapped_enc_tag"
]


def generate_enc_tag() -> str:
    return uuid.uuid4().hex


def enc_tag_delimiters() -> tuple[str, str]:
    return "[ENC_ID>", "<ID_END]"


def validate_enc_tag(tag: str, check_delimiters: bool = True) -> str | None:
    if check_delimiters:
        prefix, suffix, = enc_tag_delimiters()
        if not tag.startswith(prefix):
            return None
        elif not tag.endswith(suffix):
            return None
        tag = tag.lstrip(prefix).rstrip(suffix)

    if not len(tag) == 32:
        return None
    elif not all([c in '0123456789abcdef' for c in tag]):
        return None
    return tag


def wrap_enc_tag(unwrapped_tag: str) -> str | None:
    if validate_enc_tag(unwrapped_tag, check_delimiters=False):
        prefix, suffix = enc_tag_delimiters()
        return f"{prefix}{unwrapped_tag}{suffix}"


def unwrap_enc_tag(wrapped_tag: str) -> str | None:
    if unwrapped_tag := validate_enc_tag(wrapped_tag):
        return unwrapped_tag


def sanitize_wrapped_enc_tag(dirty_tag: str) -> str | None:
    start_index = dirty_tag.find('[')
    end_index = dirty_tag.rfind(']')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return dirty_tag[start_index:end_index + 1]
    return None
