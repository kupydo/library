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
from dotmap import DotMap


__all__ = [
	"get_pc_opsys_arch",
	"opsys_binary_name"
]


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


def opsys_binary_name(file_name: str) -> str:
	pc = get_pc_opsys_arch()
	if pc.opsys == 'windows':
		return file_name + '.exe'
	return file_name
