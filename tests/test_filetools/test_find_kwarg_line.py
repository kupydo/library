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
from pathlib import Path
from dotmap import DotMap


@pytest.fixture
def script() -> callable:
	def closure(username: str, password: str) -> str:
		pkgs = site.getsitepackages()
		lib = Path(__file__).parents[2].as_posix()
		pkgs.append(lib)
		return textwrap.dedent(f'''
			import sys
			for path in {pkgs}:
				sys.path.append(path)

			from kupydo.models import Secret
			from kupydo.internal import tools
			from kupydo.internal import errors

			auth = Secret.BasicAuth(
				username="{username}",
				password="{password}",
				name="login"
			)
			print(auth.values.string_data)
		''')
	return closure


def test_absolute_file_path(tmp_path, script):
	username = "asdfg"
	password = "qwerty"

	script = script(username, password)
	script_path = tmp_path / "test_script.py"
	script_path.write_text(script)
	result = subprocess.run(
		['python', script_path],
		capture_output=True,
		text=True
	)
	stdout = result.stdout.strip()
	obj: DotMap = eval(stdout)

	assert obj.username == username, \
		"Expected username does not match the returned username"
	assert obj.password == password, \
		"Expected password does not match the returned password"
