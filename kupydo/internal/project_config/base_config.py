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
import orjson
from pathlib import Path
from pydantic import BaseModel, field_validator
from abc import ABC, abstractmethod


__all__ = ["DeploymentBaseData", "ProjectBaseConfig"]


class DeploymentBaseData(BaseModel):
	id: str

	@field_validator("id")
	@classmethod
	def validate_id(cls, v: str) -> str:
		assert len(v) == 32, \
			"id length must equal 32 characters."
		assert all(c in '0123456789abcdef' for c in v), \
			"id must consist of valid hex characters."
		return v


class ProjectBaseConfig(ABC, BaseModel):
	def __init__(self) -> None:
		super().__init__(**self._read())

	@staticmethod
	@abstractmethod
	def _get_config_path() -> Path: ...

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
		config = self.__class__()
		for k, v in vars(config).items():
			setattr(self, k, v)
