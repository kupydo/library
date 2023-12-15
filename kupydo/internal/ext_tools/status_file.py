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
from kupydo.internal import errors
from .et_models import LatestRelease
from .local_utils import *


__all__ = ["StatusFile"]


class StatusFile(DotMap):
	@staticmethod
	def _file_path() -> Path:
		return get_bin_path() / 'status.json'

	@staticmethod
	def _default() -> StatusFile:
		fields = dict(current_version='0.0.0', last_update='2000-01-01')
		return StatusFile(dict(sops=fields.copy(), age=fields.copy()))

	@classmethod
	def _validate(cls, vsf: StatusFile) -> StatusFile:
		dsf = cls._default()
		m1 = utils.match_dict_structure(vsf, dsf)
		m2 = utils.match_dict_structure(dsf, vsf)
		if not m1 or not m2:
			return dsf
		for tool in vsf.values():
			try:
				date.fromisoformat(tool.last_update)
				Version.parse(tool.current_version)
			except ValueError:
				return dsf
		return vsf

	@classmethod
	def read(cls) -> StatusFile:
		path = cls._file_path()
		with path.open('rb') as file:
			data = orjson.loads(file.read())
		tools = data.get('tools', {})
		sf = StatusFile(tools, _prevent_method_masking=True)
		return cls._validate(sf)

	def update(self, release: LatestRelease) -> None:
		try:
			tools = self._default().keys()
			if release.tool.name not in tools:
				raise ValueError
			Version.parse(release.tag)
		except ValueError:
			raise errors.BadStatusFileError
		self[release.tool.name] = DotMap(
			last_update=date.today().isoformat(),
			current_version=release.tag
		)

	def write(self) -> None:
		comment = "THIS FILE IS MANAGED BY KUPYDO. DO NOT EDIT MANUALLY!"
		with self._file_path().open('wb') as file:
			file.write(orjson.dumps(
				dict(comment=comment, tools=self.toDict()),
				option=orjson.OPT_INDENT_2
			))
