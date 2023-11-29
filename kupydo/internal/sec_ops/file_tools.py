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
import orjson
from pathlib import Path
from collections import defaultdict
from kupydo.internal import utils
from .sfd_class import *
from .src_tools import *
from .tag_utils import *


__all__ = [
    "replace_file_secret_values",
    "write_secret_store_files"
]


def replace_file_secret_values(sfd_list: list[SecretFieldDetails], decrypt: bool = False) -> None:
    secrets_by_file: dict[Path, list[SecretFieldDetails]] = defaultdict(list)
    for sfd in sfd_list:
        secrets_by_file[sfd.file_path].append(sfd)

    if not all(path.is_file() for path in secrets_by_file.keys()):
        raise FileNotFoundError("Cannot write registered secrets into missing files.")

    for path, sfd_list in secrets_by_file.items():
        with path.open('r') as file:
            lines = file.readlines()

        for sfd in sfd_list:
            parts = separate_kwarg_line(lines[sfd.line_number])
            if parts and sfd.field_keyword in parts.keyword:
                old, new = None, None

                match decrypt:
                    case False:
                        if sfd.secret_value in parts.value:
                            old, new = sfd.secret_value, wrap_enc_tag(sfd.enc_tag)
                    case True:
                        wrapped_tag = sanitize_wrapped_enc_tag(parts.value)
                        if wrapped_tag and validate_enc_tag(wrapped_tag):
                            old, new = wrapped_tag, sfd.secret_value

                if old and new:
                    lines[sfd.line_number] = ''.join([
                        parts.keyword,
                        parts.separator,
                        parts.value.replace(old, new)
                    ])

        with path.open('w') as file:
            file.writelines(lines)


def write_secret_store_files(enc_dir: Path, sfd_list: list[SecretFieldDetails]) -> None:
    for sfd in sfd_list:
        obj = sfd.model_dump(mode="json")
        rel_path = utils.repo_abs_to_rel_path(sfd.file_path)
        obj['file_path'] = rel_path

        secret_file = enc_dir / sfd.enc_tag
        secret_file.touch(exist_ok=True)

        with secret_file.open('wb') as file:
            file.write(orjson.dumps(obj))
