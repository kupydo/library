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
import shutil
import orjson
import aiohttp
import subprocess
from pathlib import Path
from semver import Version
from kupydo.internal import errors
from .local_utils import *
from .status_file import *
from .et_models import *


__all__ = [
	"find_compatible_asset",
	"fetch_latest_release",
	"download_compatible_asset",
	"install_asset",
	"uninstall_assets",
	"check_installed_version",
	"check_asset_updates"
]


def find_compatible_asset(release: LatestRelease) -> ReleaseAsset:
	pattern = r"\w+[._-]v?\d+\.\d+\.\d+[._-](.*)"
	pc = get_pc_opsys_arch()
	for asset in release.assets:
		if match := re.search(pattern, asset.name):
			parts = re.split(r"[._-]", match.group(1))
			if pc.opsys in parts and pc.arch in parts:
				return asset
			elif pc.opsys == 'windows' and 'exe' in parts:
				return asset
			elif pc.opsys == 'freebsd' and 'linux' in parts and pc.arch in parts:
				return asset
			elif pc.opsys in parts:
				return asset
	raise errors.AssetNotFoundError(
		tool=release.tool.name,
		opsys=pc.opsys,
		arch=pc.arch
	)


async def fetch_latest_release(tool: ExtTool) -> LatestRelease:
	async with aiohttp.ClientSession() as session:
		async with session.get(tool.url) as response:
			data = await response.read()
			return LatestRelease(
				**orjson.loads(data),
				tool=tool
			)


async def download_compatible_asset(rel: LatestRelease) -> Path:
	asset = find_compatible_asset(rel)
	file_path = get_bin_path() / asset.name
	async with aiohttp.ClientSession() as session:
		async with session.get(asset.url) as resp:
			with file_path.open('wb') as file:
				chunked = resp.content.iter_chunked
				async for data in chunked(1024):
					file.write(data)
	return file_path


def install_asset(tool: ExtTool, file_path: Path) -> None:
	if tool == ExtTool.SOPS:
		shutil.move(file_path, tool.path)
	elif tool == ExtTool.AGE:
		shutil.unpack_archive(
			filename=file_path,
			extract_dir=file_path.parent
		)
		file_path.unlink()
		age_dir = get_bin_path() / 'age'
		for file in age_dir.iterdir():
			if file.name == 'LICENSE':
				continue
			dest = file.parents[1] / file.name
			shutil.move(src=file, dst=dest)
		shutil.rmtree(path=age_dir)


def uninstall_assets() -> None:
	path = get_bin_path()
	for item in path.iterdir():
		if item.name == 'status.json':
			continue
		item.unlink(missing_ok=True)


def check_installed_version(tool: ExtTool, private: bool = False) -> Version | None:
	try:
		path = tool.path if private else tool.name
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


async def check_asset_updates(tool: ExtTool) -> LatestRelease | None:
	rel = await fetch_latest_release(tool)
	remote_ver = Version.parse(rel.tag)
	data = StatusFile.read().get(tool.name)
	local_ver = Version.parse(data.current_version)
	return rel if remote_ver > local_ver else None
