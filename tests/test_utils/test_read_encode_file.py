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
def script(tmp_path) -> callable:
	def closure(from_relative: bool = False) -> str:
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
				encoded = utils.read_encode_file("{
					"./test_data.py" 
					if from_relative else 
					data_path.as_posix()
				}")
				print(encoded)
	
			caller()
		''')
		data_path.write_text("Hello World")
		script_path.write_text(script)
		result = subprocess.run(
			['python', script_path],
			capture_output=True,
			text=True
		)
		return result.stdout.strip()
	return closure


@pytest.fixture
def expected_output():
	return base64.b64encode("Hello World".encode()).decode()


def test_absolute_file_path(script, expected_output):
	assert script() == expected_output, \
		"The output should be the base64 encoded string of 'Hello World'"


def test_relative_file_path(script, expected_output):
	assert script(from_relative=True) == expected_output, \
		"The output should be the base64 encoded string of 'Hello World'"
