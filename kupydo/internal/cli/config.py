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
from pathlib import Path
from pydantic import BaseModel, field_validator
from kupydo.internal import utils


CONFIG_FILE_NAME = '.kupydo'


class KupydoDeploymentDetails(BaseModel):
	name: str
	path: str
	pubkey: str

	@field_validator("name")
	@classmethod
	def validate_name(cls, v: str) -> str:
		assert len(v) <= 20, "name must be less than or equal to 20 characters."
		assert v.isalnum(), "name must consist of alphanumeric characters: a-z, 0-9."
		return v

	@field_validator("path", mode="before")
	@classmethod
	def validate_path(cls, v: str) -> str:
		path = utils.repo_rel_to_abs_path(v)
		assert path.is_file(), "path cannot point to a non-existent file."
		assert path.name == "Heart.py", "path must point to a file named 'Heart.py'."
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


class KupydoConfig(BaseModel):
	deployments: list[KupydoDeploymentDetails]

	def __init__(self) -> None:
		super().__init__(**self._read())

	@staticmethod
	def _get_config_path() -> Path:
		repo_path = utils.find_repo_path()
		config_path = repo_path / CONFIG_FILE_NAME
		config_path.touch(exist_ok=True)
		return config_path

	@classmethod
	def _read(cls) -> dict:
		path = cls._get_config_path()
		with path.open('rb') as file:
			contents = file.read() or b'{}'
		return orjson.loads(contents)

	def write(self) -> None:
		path = self._get_config_file_path()
		dump = orjson.dumps(
			self.model_dump(mode='json'),
			option=orjson.OPT_INDENT_2
		)
		with path.open('wb') as file:
			file.write(dump)

	def update(self) -> None:
		config = KupydoConfig()
		for k, v in vars(config).items():
			setattr(self, k, v)
