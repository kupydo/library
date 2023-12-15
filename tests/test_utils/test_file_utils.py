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
import site
import base64
import pytest
import textwrap
import subprocess
from pathlib import Path
from kupydo.internal import errors
from kupydo.internal import utils


@pytest.fixture(name="create_tmp_file")
def fixture_create_tmp_file(tmp_path: Path):
	def create_file(content, filename="temp_file.txt"):
		file_path = tmp_path / filename
		file_path.write_text(content)
		return file_path
	return create_file


def test_file_lines(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)
	expected_output = ["Line 1\n", "Line 2\n", "Line 3"]
	assert utils.read_cached_file_lines(file_path) == expected_output, \
		"Function should correctly read file lines"
	utils.read_cached_file_lines.cache_clear()


def test_same_file(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)

	first_call_result = utils.read_cached_file_lines(file_path)
	second_call_result = utils.read_cached_file_lines(file_path)

	assert utils.read_cached_file_lines.cache_info().hits == 1
	assert first_call_result is second_call_result, \
		"Function should return cached result on subsequent calls with same file"
	utils.read_cached_file_lines.cache_clear()


def test_after_file_change(create_tmp_file):
	content = "Line 1\nLine 2\nLine 3"
	file_path = create_tmp_file(content)

	initial_result = utils.read_cached_file_lines(file_path)

	new_content = "New Line 1\nNew Line 2\nNew Line 3"
	file_path.write_text(new_content)

	updated_result = utils.read_cached_file_lines(file_path)

	assert initial_result == updated_result, \
		"Function should not detect file content change due to caching"
	utils.read_cached_file_lines.cache_clear()


def test_relative_file_path(tmp_path: Path):
	pkgs = site.getsitepackages()
	lib = Path(__file__).parents[2].as_posix()
	pkgs.append(lib)

	data_path = tmp_path / "test_data.py"
	script_path = tmp_path / "test_script.py"

	script = textwrap.dedent(f'''
		import sys
		for path in {pkgs}:
			sys.path.append(path)

		from kupydo.internal import utils

		def caller():
			encoded = utils.read_encode_rel_file("test_data.py")
			print(encoded)

		caller()
	''')
	data_path.write_text("Hello World")
	script_path.write_text(script)
	result = subprocess.run(
		args=['python', script_path],
		capture_output=True,
		text=True
	)
	expected_result = base64.b64encode("Hello World".encode()).decode()
	assert result.stdout.strip() == expected_result, \
		"The output should be the base64 encoded string of 'Hello World'"


def test_absolute_file_path():
	with pytest.raises(errors.PathNotRelativeError):
		abs_path = Path(__file__).resolve().as_posix()
		utils.read_encode_rel_file(abs_path)
