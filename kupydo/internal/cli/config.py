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
from kupydo.internal.cli import utils
from kupydo.internal.cli.classes import KupydoConfig


def get_config_file_path() -> Path:
    return utils.find_repo_path() / '.kupydo'


def read_config_file() -> KupydoConfig:
    path = get_config_file_path()
    path.touch(exist_ok=True)
    with path.open('rb') as file:
        contents = file.read() or "{}"
    obj = orjson.loads(contents)
    return KupydoConfig(**obj)


def write_config_file(config: KupydoConfig):
    path = get_config_file_path()
    dump = orjson.dumps(
        config.model_dump(mode='json'),
        option=orjson.OPT_INDENT_2
    )
    with path.open('wb') as file:
        file.write(dump)
