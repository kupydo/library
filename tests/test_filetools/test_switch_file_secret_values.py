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
from kupydo.internal import tools


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
	
			from kupydo.internal import tools
			from kupydo.models import Secret
			from kupydo import GlobalRegistry
			
			GlobalRegistry.set_enabled(state=True)
			Secret.BasicAuth(
				username="{username}",
				password="{password}",
				name="login"
			)
			secrets = GlobalRegistry.get_all_secrets()
			tools.switch_file_secret_values(secrets)
			for sec in secrets:
				print(sec.field_keyword, sec.identifier)
		''')
	return closure


def test_first_external_caller(tmp_path: Path, script: callable):
	username = "secret-username"
	password = "secret-password"

	script = script(username, password)
	script_path = tmp_path / "test_script.py"
	script_path.write_text(script)
	result = subprocess.run(
		['python', script_path],
		capture_output=True,
		text=True
	)
	with script_path.open('r') as file:
		lines = file.readlines()

	block = tools.extract_caller_block(lines, 11)
	for kwd_sid in result.stdout.strip().split('\n'):
		keyword, sid = kwd_sid.split(' ')
		found = False
		for line in lines[block.start:block.end]:
			if keyword in line and sid in line:
				found = True

		assert found is True, "Process output does not match file contents"
