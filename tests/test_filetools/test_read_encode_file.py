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
import pytest
import textwrap
import subprocess
import base64
from pathlib import Path


@pytest.fixture
def script() -> str:
	pkgs = site.getsitepackages()
	lib = Path(__file__).parents[2].as_posix()
	pkgs.append(lib)
	return textwrap.dedent(f'''
		import sys
		for path in {pkgs}:
			sys.path.append(path)

		from kupydo.internal import tools

		def caller():
			with open("{{file_write_path}}", "w") as f:
				f.write("{{data_to_write}}")
			encoded = tools.read_encode_file("{{file_read_path}}")
			print(encoded)

		caller()
	''')


def test_absolute_file_path(script, tmp_path):
	test_script = tmp_path / "test_script.py"
	data_path = (tmp_path / "test_data.py").as_posix()
	test_script.write_text(script.format(
		file_write_path=data_path,
		file_read_path=data_path,
		data_to_write="Hello World"
	))

	result = subprocess.run(['python', test_script], capture_output=True, text=True)
	output = result.stdout.strip()

	expected_output = base64.b64encode("Hello World".encode()).decode()
	assert output == expected_output, \
		"The output should be the base64 encoded string of 'Hello World'"


def test_relative_file_path(script, tmp_path):
	test_script = tmp_path / "test_script.py"
	test_script.write_text(script.format(
		file_write_path=(tmp_path / "test_data.py").as_posix(),
		file_read_path="./test_data.py",
		data_to_write="Hello World"
	))

	result = subprocess.run(['python', test_script], capture_output=True, text=True)
	output = result.stdout.strip()

	expected_output = base64.b64encode("Hello World".encode()).decode()
	assert output == expected_output, \
		"The output should be the base64 encoded string of 'Hello World'"
