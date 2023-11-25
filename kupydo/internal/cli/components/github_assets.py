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
from __future__ import annotations
import re
import shutil
import orjson
import aiohttp
from enum import Enum
from typing import Annotated
from pathlib import Path
from datetime import datetime, date
from pydantic import (
	Field,
	BaseModel,
	field_validator,
	model_validator
)
from kupydo.internal import utils
from kupydo.internal.errors import *


__all__ = [
	"CryptoTool",
	"AssetType",
	"ReleaseAsset",
	"LatestRelease",
	"find_compatible_asset",
	"fetch_latest_release",
	"download_compatible_asset",
	"install_asset"
]


class CryptoTool(str, Enum):
	SOPS = "https://api.github.com/repos/getsops/sops/releases/latest"
	AGE = "https://api.github.com/repos/FiloSottile/age/releases/latest"


class AssetType(str, Enum):
	ARCHIVE = 'archive'
	BINARY = 'binary'


class ReleaseAsset(BaseModel):
	name: str
	type: Annotated[AssetType | None, Field(alias="content_type")]
	url: Annotated[str, Field(alias="browser_download_url")]

	@field_validator("name", mode="after")
	@classmethod
	def validate_name(cls, v: str) -> str:
		assert re.match(r"\w+[._-]v?\d+\.\d+\.\d+[._-].*", v), \
			"The asset name does not match the expected pattern"
		return v

	@field_validator("type", mode="before")
	@classmethod
	def validate_type(cls, v: str) -> AssetType | None:
		return AssetType.BINARY if v in [
			"application/x-ms-dos-executable",  # Windows
			"application/octet-stream",  # Darwin & Linux
		] else AssetType.ARCHIVE if v in [
			"application/x-gtar",  # .tar.gz
			"application/zip"  # .zip
		] else None

	@model_validator(mode="after")
	def validate_url(self) -> ReleaseAsset:
		pattern = rf'https://github\.com/\w+/\w+/releases/download/v?\d+\.\d+\.\d+/{re.escape(self.name)}'
		assert re.match(pattern, self.url), "The asset url does not match the expected pattern"
		return self


class LatestRelease(BaseModel):
	tool: CryptoTool
	tag: Annotated[str, Field(alias="tag_name")]
	date: Annotated[date, Field(alias="published_at")]
	assets: list[ReleaseAsset]

	@field_validator("tag", mode="after")
	@classmethod
	def validate_tag_name(cls, v: str) -> str:
		assert re.match(r"v\d+\.\d+\.\d+", v), \
			"The version tag does not match the expected pattern"
		return v

	@field_validator("date", mode="before")
	@classmethod
	def validate_published_at(cls, v: str) -> date:
		return datetime.fromisoformat(v).date()

	@field_validator("assets", mode="after")
	@classmethod
	def validate_assets(cls, v: list[ReleaseAsset]) -> list[ReleaseAsset]:
		return [
			item for item in v if
			item.type is not None and
			'json' not in item.name
		]


def find_compatible_asset(release: LatestRelease) -> ReleaseAsset:
	pattern = r"\w+[._-]v?\d+\.\d+\.\d+[._-](.*)"
	pc = utils.get_pc_opsys_arch()
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
	raise AssetNotFoundError(
		tool=release.tool.name.lower(),
		opsys=pc.opsys,
		arch=pc.arch
	)


async def fetch_latest_release(tool: CryptoTool) -> LatestRelease:
	async with aiohttp.ClientSession() as session:
		async with session.get(tool.value) as response:
			data = await response.read()
			return LatestRelease(
				**orjson.loads(data),
				tool=tool
			)


async def download_compatible_asset(rel: LatestRelease) -> Path:
	asset = find_compatible_asset(rel)
	file_path = utils.find_bin_path() / asset.name
	async with aiohttp.ClientSession() as session:
		async with session.get(asset.url) as resp:
			with file_path.open('wb') as file:
				chunked = resp.content.iter_chunked
				async for data in chunked(1024):
					file.write(data)
	return file_path


def install_asset(tool: CryptoTool, file_path: Path) -> None:
	if tool == CryptoTool.SOPS:
		file_name = utils.opsys_binary_name('sops')
		new_path = file_path.parent / file_name
		shutil.move(file_path, new_path)
	elif tool == CryptoTool.AGE:
		shutil.unpack_archive(
			filename=file_path,
			extract_dir=file_path.parent
		)
		file_path.unlink()

		age_keygen_file = utils.opsys_binary_name('age-keygen')
		age_file = utils.opsys_binary_name('age')

		shutil.move(
			src=file_path.parent / 'age' / age_keygen_file,
			dst=file_path.parent / age_keygen_file
		)
		shutil.move(
			src=file_path.parent / 'age' / age_file,
			dst=file_path.parent / age_file
		)
		shutil.rmtree(
			path=file_path.parent / 'age',
			ignore_errors=True
		)
