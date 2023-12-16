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
from pydantic import BaseModel, field_validator
from kupydo.internal import utils


__all__ = ["SecretFieldDetails"]


class SecretFieldDetails(BaseModel):
    enc_tag: str
    file_path: Path
    line_number: int
    field_keyword: str
    field_value: str
    secret_value: str
    from_file: bool

    @field_validator("file_path", mode="before")
    @classmethod
    def convert_file_path(cls, v: str) -> Path:
        if not utils.is_path_absolute(v):
            return utils.repo_rel_to_abs_path(v)
        return Path(v)
