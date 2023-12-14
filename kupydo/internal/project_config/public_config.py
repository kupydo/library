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
import orjson
import string
from pathlib import Path, PurePosixPath, PureWindowsPath
from pydantic import BaseModel, field_validator, model_validator
from kupydo.internal import utils


__all__ = ["DeploymentPublicDetails", "ProjectPublicConfig"]


class DeploymentPublicDetails(BaseModel):
	id: str
	alias: str
	path: str
	pubkey: str

	@field_validator("id")
	@classmethod
	def validate_id(cls, v: str) -> str:
		assert len(v) == 32, \
			"id length must equal 32 characters."
		assert all(c in '0123456789abcdef' for c in v), \
			"id must consist of valid hex characters."
		return v

	@field_validator("alias")
	@classmethod
	def validate_alias(cls, v: str) -> str:
		valid_chars = string.ascii_letters + string.digits + '-'
		assert len(v) <= 20, \
			"alias length must be less than or equal to 20 characters."
		assert all(c in valid_chars for c in v), \
			"alias must consist of any valid characters: a-z, A-Z, 0-9, '-'."
		return v

	@field_validator("path", mode="before")
	@classmethod
	def validate_path(cls, v: str) -> str:
		is_abs_pp = PurePosixPath(v).is_absolute()
		is_abs_wp = PureWindowsPath(v).is_absolute()
		assert not any([is_abs_pp, is_abs_wp]), \
			"path must be a relative path."
		path = utils.repo_rel_to_abs_path(v)
		assert path.is_file(), \
			"path cannot point to a non-existent file."
		assert path.name == "Heart.py", \
			"path must point to a file named 'Heart.py'."
		return v

	@field_validator("pubkey")
	@classmethod
	def validate_pubkey(cls, v: str) -> str:
		allowed_pattern = r'^age[0-9a-z]{59}$'
		forbidden_pattern = r"^AGE-SECRET-KEY-[0-9A-Z]{59}$"
		assert re.match(forbidden_pattern, v) is None, \
			"not allowed to assign an AGE secret key to the pubkey field."
		assert re.match(allowed_pattern, v) is not None, \
			"must assign a valid AGE public key to the pubkey field."
		return v


class ProjectPublicConfig(BaseModel):
	deployments: list[DeploymentPublicDetails]

	@model_validator(mode="before")
	@classmethod
	def check_duplicates(cls, data: dict) -> dict:
		if data:
			for key in ["id", "alias", "path", "pubkey"]:
				ids = [item[key] for item in data["deployments"]]
				assert len(set(ids)) == len(ids), \
					f"duplicate {key} values not allowed in public config file."
		return data

	def __init__(self) -> None:
		super().__init__(**self._read())

	@staticmethod
	def _get_config_path() -> Path:
		repo_path = utils.find_repo_path()
		config_path = repo_path / '.kupydo'
		config_path.touch(exist_ok=True)
		return config_path

	@classmethod
	def _read(cls) -> dict:
		path = cls._get_config_path()
		with path.open('rb') as file:
			contents = file.read() or b'{}'
		return orjson.loads(contents)

	def write(self) -> None:
		path = self._get_config_path()
		dump = orjson.dumps(
			self.model_dump(mode='json'),
			option=orjson.OPT_INDENT_2
		)
		with path.open('wb') as file:
			file.write(dump)

	def update(self) -> None:
		config = ProjectPublicConfig()
		for k, v in vars(config).items():
			setattr(self, k, v)
