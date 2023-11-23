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
import pytest
from pathlib import Path
from kupydo.internal import tools


@pytest.fixture
def temp_file(tmp_path: Path):
    def create_file(content, filename="temp_file.txt"):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return file_path
    return create_file


def test_file_lines(temp_file):
    content = "Line 1\nLine 2\nLine 3"
    file_path = temp_file(content)
    expected_output = ["Line 1\n", "Line 2\n", "Line 3"]
    assert tools.read_cached_file_lines(file_path) == expected_output, \
        "Function should correctly read file lines"
    tools.read_cached_file_lines.cache_clear()


def test_same_file(temp_file):
    content = "Line 1\nLine 2\nLine 3"
    file_path = temp_file(content)

    first_call_result = tools.read_cached_file_lines(file_path)
    second_call_result = tools.read_cached_file_lines(file_path)

    assert tools.read_cached_file_lines.cache_info().hits == 1
    assert first_call_result is second_call_result, \
        "Function should return cached result on subsequent calls with same file"
    tools.read_cached_file_lines.cache_clear()


def test_after_file_change(temp_file):
    content = "Line 1\nLine 2\nLine 3"
    file_path = temp_file(content)

    initial_result = tools.read_cached_file_lines(file_path)

    new_content = "New Line 1\nNew Line 2\nNew Line 3"
    file_path.write_text(new_content)

    updated_result = tools.read_cached_file_lines(file_path)

    assert initial_result == updated_result, \
        "Function should not detect file content change due to caching"
    tools.read_cached_file_lines.cache_clear()
