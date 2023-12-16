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
import string
from pathlib import Path
from pydantic import field_validator, model_validator
from kupydo.internal import utils
from .base_config import *


__all__ = ["DeploymentPublicData", "ProjectPublicConfig"]


class DeploymentPublicData(DeploymentBaseData):
	alias: str
	path: str
	pubkey: str

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
		assert not utils.is_path_absolute(v), \
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


class ProjectPublicConfig(ProjectBaseConfig):
	deployments: list[DeploymentPublicData]

	@model_validator(mode="before")
	@classmethod
	def check_duplicates(cls, data: dict) -> dict:
		if data:
			for key in ["alias", "path", "pubkey"]:
				values = [item[key] for item in data["deployments"]]
				assert len(set(values)) == len(values), \
					f"duplicate {key} values not allowed in public config file."
		return data

	@staticmethod
	def get_config_path() -> Path:
		repo_path = utils.find_repo_path()
		config_path = repo_path / '.kupydo'
		config_path.touch(exist_ok=True)
		return config_path
