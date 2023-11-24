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
import re
from dotmap import DotMap
from kupydo.internal.errors import *


__all__ = [
    "extract_caller_block",
    "separate_kwarg_line",
    "kwarg_regex_pattern",
    "find_kwarg_line"
]


def extract_caller_block(lines: list[str], lineno: int) -> DotMap | None:
    start = lineno - 1 if lineno > 0 else 0
    open_parens, close_parens = 0, 0

    for i, line in enumerate(lines[start:], start=start):
        open_parens += line.count('(')
        close_parens += line.count(')')
        if open_parens == 0 and close_parens > 0:
            break
        elif open_parens > 0 and open_parens == close_parens:
            return DotMap(start=start, end=i)
    return None


def separate_kwarg_line(line: str) -> DotMap | None:
    separator = None
    if ':' in line and '=' in line:
        separator = '=' if line.index('=') < line.index(':') else ':'
    elif ':' in line:
        separator = ':'
    elif '=' in line:
        separator = '='

    if separator:
        keyword, value = line.split(separator, 1)
        if not keyword or not value:
            return None
        return DotMap(
            keyword=keyword,
            separator=separator,
            value=value
        )
    return None


def kwarg_regex_pattern(line: str, keyword: str, value: str) -> str | None:
    if parts := separate_kwarg_line(line):
        kwd, val = re.escape(keyword), re.escape(value)
        if parts.separator == '=':
            return rf"^\s*{kwd}\s*=\s*['\"]{val}['\"].*\s*$"
        elif parts.separator == ':':
            return rf"^\s*['\"]{kwd}['\"]\s*:\s*['\"]{val}['\"].*\s*$"
    return None


def find_kwarg_line(lines: list[str], from_line: int, keyword: str, value: str) -> int:
    if block := extract_caller_block(lines, from_line):
        s, e = block.start, block.end
        for i, line in enumerate(lines[s:e + 1], start=s):
            if pattern := kwarg_regex_pattern(line, keyword, value):
                if re.search(pattern, line):
                    return i
    raise KwargNotFoundError(keyword, value)  # pragma: no cover
