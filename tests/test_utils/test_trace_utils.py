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


@pytest.fixture(name="script")
def fixture_script() -> str:
	pkgs = site.getsitepackages()
	lib = Path(__file__).parents[2].as_posix()
	pkgs.append(lib)
	return textwrap.dedent(f'''
		import sys
		for path in {pkgs}:
			sys.path.append(path)
		
		from kupydo.internal import utils
		
		def caller():
			print(utils.first_external_caller())
		
		caller()
	''')


def test_first_external_caller(tmp_path: Path, script: str):
	temp_script = tmp_path / "test_script.py"
	temp_script.write_text(script)

	result = subprocess.run(['python', temp_script], capture_output=True, text=True)
	output = result.stdout.strip().split('\n')[-1]
	output = output.replace("PosixPath(", "Path(").replace("WindowsPath(", "Path(")
	output_path, line_number = eval(output)

	assert temp_script.resolve() == output_path, \
		"The path should match the path of the temporary script"
	assert line_number == 9, \
		"The line number should correspond to the line where first_external_caller is called in the script"
