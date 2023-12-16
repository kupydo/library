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
from typing import Callable
from kupydo.internal import errors
from kupydo.internal import utils


@pytest.fixture(name="create_tmp_file")
def fixture_create_tmp_file(tmp_path: Path):
	def create_file(content: str = None):
		file_path = tmp_path / "tmp_file.txt"
		file_path.touch()
		if content:
			file_path.write_text(content)
		return file_path
	return create_file


def test_read_encode_b64_file(create_tmp_file: Callable):
	path = create_tmp_file("Hello World")
	result = utils.read_encode_b64_file(path)
	assert result == "SGVsbG8gV29ybGQ="


def test_write_decode_b64_file(create_tmp_file: Callable):
	path = create_tmp_file()
	utils.write_decode_b64_file(path, "SGVsbG8gV29ybGQ=")
	assert path.read_text() == "Hello World"


def test_read_encode_b64_file_invalid_rel_path():
	for inv_path in ["./home/user/file", "home/user/file"]:
		with pytest.raises(errors.InvalidPathTypeError):
			utils.read_encode_b64_file(inv_path)


def test_write_decode_b64_file_invalid_rel_path():
	for inv_path in ["./home/user/file", "home/user/file"]:
		with pytest.raises(errors.InvalidPathTypeError):
			utils.write_decode_b64_file(inv_path, '')


def test_read_cached_file_lines(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)
	expected_output = ["Line 1\n", "Line 2\n", "Line 3"]
	assert utils.read_cached_file_lines(file_path) == expected_output, \
		"Function should correctly read file lines"
	utils.read_cached_file_lines.cache_clear()


def test_read_cached_same_file(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)

	first_call_result = utils.read_cached_file_lines(file_path)
	second_call_result = utils.read_cached_file_lines(file_path)

	assert utils.read_cached_file_lines.cache_info().hits == 1
	assert first_call_result is second_call_result, \
		"Function should return cached result on subsequent calls with same file"
	utils.read_cached_file_lines.cache_clear()


def test_read_cached_after_file_change(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)

	initial_result = utils.read_cached_file_lines(file_path)

	new_content = "New Line 1\nNew Line 2\nNew Line 3"
	file_path.write_text(new_content)

	updated_result = utils.read_cached_file_lines(file_path)

	assert initial_result == updated_result, \
		"Function should not detect file content change due to caching"
	utils.read_cached_file_lines.cache_clear()
