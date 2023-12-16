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
from kupydo.internal import sec_ops


@pytest.fixture(name="script")
def fixture_script() -> str:
	pkgs = site.getsitepackages()
	lib = Path(__file__).parents[3].as_posix()
	pkgs.append(lib)
	return textwrap.dedent(f'''
		import sys
		for path in {pkgs}:
			sys.path.append(path)
		from kupydo.internal import sec_ops
		from kupydo.models import Secret
		from kupydo import GlobalRegistry
		
		GlobalRegistry.set_enabled(True)
		GlobalRegistry.set_silent(True)
		sec = Secret.BasicAuth(
			username="secret-name-123",
			password="secret-pass-456",
			name="login"
		)
		secrets = GlobalRegistry.get_all_secrets()
		sec_ops.replace_file_secret_values(secrets)
		for sec in secrets:
			print(sec.field_keyword, sec.enc_tag)
	''')


def test_replace_file_secret_values(tmp_path: Path, script: str):
	script_file = tmp_path / "test_script.py"
	script_file.write_text(script)
	result = subprocess.run(
		['python', script_file],
		capture_output=True,
		text=True
	)
	with script_file.open('r') as file:
		lines = file.readlines()

	block = sec_ops.extract_caller_block(lines, 11)
	for res_line in result.stdout.strip().split('\n'):
		keyword, enc_tag = res_line.split(' ')
		found = False
		for line in lines[block.start:block.end]:
			if keyword in line and enc_tag in line:
				found = True

		assert found is True, "Process output does not match file contents"
