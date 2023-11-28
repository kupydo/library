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
import inspect
import linecache
from pathlib import Path
from types import TracebackType
from .path_utils import find_lib_path


__all__ = [
    "extract_tb_line",
    "extract_tb_filepath",
    "first_external_caller"
]


def extract_tb_line(tb: TracebackType) -> str:
    path = Path(tb.tb_frame.f_code.co_filename).as_posix()
    return linecache.getline(path, tb.tb_lineno).strip()


def extract_tb_filepath(tb: TracebackType) -> str:
    path = Path(tb.tb_frame.f_code.co_filename)
    try:
        index = path.parts.index('kupydo')
        path = Path(*path.parts[index:])
    except ValueError:
        pass
    return path.as_posix()


def first_external_caller() -> tuple[Path, int]:
    lib_path = find_lib_path()
    for frame_info in inspect.stack():
        frame_file_path = Path(frame_info.filename)

        # always evaluates to true eventually
        if not frame_file_path.is_relative_to(lib_path):
            return frame_file_path, frame_info.lineno
