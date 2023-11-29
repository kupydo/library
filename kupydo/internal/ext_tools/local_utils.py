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
import sys
import platform
from pathlib import Path
from dotmap import DotMap


__all__ = [
	"get_bin_path",
	"get_tool_posix_path",
	"bin_opsys_name",
	"get_pc_opsys_arch"
]


def get_bin_path() -> Path:
	return Path(__file__).parent / "bin"


def get_tool_posix_path(name: str) -> str | None:
	path = get_bin_path() / bin_opsys_name(name)
	return path.as_posix() if path.is_file() else None


def bin_opsys_name(file_name: str) -> str:
	pc = get_pc_opsys_arch()
	if pc.opsys == 'windows':
		return file_name + '.exe'
	return file_name


def get_pc_opsys_arch() -> DotMap:
	opsys = sys.platform.lower()
	if opsys in ['darwin', 'freebsd']:
		pass
	elif opsys.startswith('linux'):
		opsys = 'linux'
	elif opsys == 'win32':
		opsys = 'windows'

	arch = platform.machine().lower()
	if arch in ['x86_64', 'amd64']:
		arch = 'amd64'
	elif arch in ['aarch64', 'arm64']:
		arch = 'arm64'
	elif arch.startswith('arm'):
		arch = 'arm'

	return DotMap(opsys=opsys, arch=arch)
