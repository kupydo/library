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
from enum import Enum
from typing import Annotated
from datetime import datetime, date
from pydantic import (
	Field,
	BaseModel,
	field_validator,
	model_validator
)


__all__ = [
	"ExtTool",
	"AssetType",
	"ReleaseAsset",
	"LatestRelease"
]


class ExtTool(str, Enum):
	SOPS = "https://api.github.com/repos/getsops/sops/releases/latest"
	AGE = "https://api.github.com/repos/FiloSottile/age/releases/latest"

	@property
	def name(self) -> str:
		return self._name_.lower()


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
	tool: ExtTool
	tag: Annotated[str, Field(alias="tag_name")]
	date: Annotated[date, Field(alias="published_at")]
	assets: list[ReleaseAsset]

	@field_validator("tag", mode="after")
	@classmethod
	def validate_tag_name(cls, v: str) -> str:
		assert re.match(r"v?\d+\.\d+\.\d+", v), \
			"The version tag does not match the expected pattern"
		return v.lstrip('v')

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
