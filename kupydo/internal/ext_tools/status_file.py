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
from semver import Version
from pathlib import Path
from datetime import date
from kupydo.internal import utils
from kupydo.internal.errors import BadStatusFileError
from .classes import LatestRelease, ExtTool


__all__ = ["StatusFile"]


class StatusFile(DotMap):
	@staticmethod
	def _file_path() -> Path:
		return utils.find_bin_path() / 'status.json'

	@staticmethod
	def _default() -> dict:
		comment = "THIS FILE IS MANAGED BY KUPYDO. DO NOT EDIT MANUALLY!"
		default = dict(current_version='0.0.0', last_update='2000-01-01')
		return dict(
			comment=comment,
			tools=dict(
				sops=default.copy(),
				age=default.copy()
			)
		)

	@classmethod
	def _validate(cls, sf: StatusFile) -> bool:
		for k, v in cls._default().items():
			if k not in sf:
				return False
			elif k == 'comment' and sf[k] != v:
				return False

		for asset in [ExtTool.SOPS, ExtTool.AGE]:
			data = sf['tools'][asset.name]
			cv = data['current_version']
			lu = data['last_update']
			try:
				date.fromisoformat(lu)
				Version.parse(cv)
			except ValueError:
				return False
		return True

	@classmethod
	def read(cls) -> StatusFile:
		path = cls._file_path()
		with path.open('rb') as file:
			data = orjson.loads(file.read())
		sf = StatusFile(data)
		if not cls._validate(sf):
			data = cls._default()
			sf = StatusFile(data)
		return sf

	def update(self, releases: tuple[LatestRelease]) -> None:
		for rel in releases:
			self[rel.tool.name] = DotMap(
				last_update=date.today().isoformat(),
				current_version=rel.tag
			)

	def write(self) -> None:
		if not self._validate(self):
			raise BadStatusFileError
		path = self._file_path()
		with path.open('wb') as file:
			file.write(orjson.dumps(
				self.toDict(),
				option=orjson.OPT_INDENT_2
			))
