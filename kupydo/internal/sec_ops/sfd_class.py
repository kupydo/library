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
from pydantic import BaseModel


__all__ = ["SecretFieldDetails"]


class SecretFieldDetails(BaseModel):
    file_path: Path
    line_number: int
    field_keyword: str
    field_value: str
    secret_value: str
    enc_tag: str
