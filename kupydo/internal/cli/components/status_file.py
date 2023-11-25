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
from dotmap import DotMap
from pathlib import Path
from datetime import date
from kupydo.internal import utils
from .github_assets import LatestRelease


__all__ = ["StatusFile"]


class StatusFile(DotMap):
	@staticmethod
	def _file_path() -> Path:
		return utils.find_bin_path() / 'status.json'

	@classmethod
	def read(cls) -> StatusFile:
		path = cls._file_path()
		with path.open('rb') as file:
			data = orjson.loads(file.read())
		return StatusFile(**data)

	def update(self, releases: tuple[LatestRelease]) -> None:
		for rel in releases:
			self[rel.tool.name.lower()] = DotMap(
				last_update=date.today().isoformat(),
				current_version=rel.tag
			)

	def write(self) -> None:
		path = self._file_path()
		with path.open('wb') as file:
			file.write(orjson.dumps(
				self.toDict(),
				option=orjson.OPT_INDENT_2
			))
