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
import re
import subprocess
from semver import Version
from kupydo.internal import utils
from .github_assets import *
from .status_file import *


__all__ = [
	"check_tool_version",
	"check_tool_updates"
]


def check_tool_version(tool: CryptoTool, private: bool = False) -> Version | None:
	try:
		path = utils.opsys_binary_name(tool.name.lower())
		if private:
			path = utils.find_bin_path() / path
		result = subprocess.run(
			args=[path, '--version'],
			capture_output=True,
			text=True
		)
		pattern = r"v?\d+\.\d+\.\d+"
		if match := re.search(pattern, result.stdout):
			version = match.group().lstrip('v')
			return Version.parse(version)
	except (OSError, FileNotFoundError):
		return None
	return None


async def check_tool_updates(tool: CryptoTool) -> LatestRelease | None:
	rel = await fetch_latest_release(tool)
	remote_ver = Version.parse(rel.tag.lstrip('v'))
	tool_data = StatusFile.read()[tool.name.lower()]
	local_ver = Version.parse(tool_data.current_version.lstrip('v'))
	return rel if remote_ver > local_ver else None
