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
import os
import pytest
import orjson
from pathlib import Path
from dotmap import DotMap
from typing import Callable, Literal
from kupydo.internal.project_config import *


@pytest.fixture(name="depl")
def fixture_depl() -> DotMap:
	return DotMap(
		first={
			"id": "c5027735a24c3daa00fbc655b8aa20f3",
			"alias": "MyApp123-dev",
			"path": "clusters/dev/Heart.py",
			"pubkey": "age17qyz09pyjxfwyxdjwyugw7wxy8gtk0gc23t7y9qqxccg6hr8uyqsqlmh2k"
		},
		second={
			"id": "846ef331b4e9df983d8e6b9905d518e1",
			"alias": "MyApp123-prod",
			"path": "clusters/prod/Heart.py",
			"pubkey": "age1v0rxka5x7haf928yszv97eprf726fnwdqklnpf88frqqgec9mqysuzj9q6"
		}
	)


@pytest.fixture(name="temp_repo")
def fixture_temp_repo(tmp_path: Path, depl: DotMap) -> Callable:
	os.chdir(tmp_path)
	(tmp_path / ".git").mkdir()
	for cluster in ["dev", "prod"]:
		path = tmp_path / f"clusters/{cluster}"
		path.mkdir(parents=True)
		(path / "Heart.py").touch()

	dkt = Literal["alias", "path", "pubkey"]

	def custom_kupydo_file(garbage: bool = False, dupe_key: dkt = None):
		kupydo_file = tmp_path / ".kupydo"
		with kupydo_file.open("w") as file:
			if garbage:
				content = '{"deployments" : [error]}'
			else:
				content = orjson.dumps({
					"deployments": [
						depl.first,
						depl.second if not dupe_key else {
							**depl.second,
							dupe_key: depl.first[dupe_key]
						}
					]
				}).decode("utf-8")
			file.write(content)

	return custom_kupydo_file


def test_read_file_contents(temp_repo: Callable, depl: DotMap):
	temp_repo()
	conf = ProjectPublicConfig()
	for pd, fd in zip(conf.deployments, depl.values()):
		for key in ["id", "alias", "path", "pubkey"]:
			assert getattr(pd, key) == fd[key]


def test_write_and_update(temp_repo: Callable, depl: DotMap):
	temp_repo()
	new_alias = "456-NewAlias"

	conf1 = ProjectPublicConfig()
	assert conf1.deployments[0].alias == depl.first["alias"]
	assert conf1.deployments[1].alias == depl.second["alias"]

	conf2 = ProjectPublicConfig()
	conf2.deployments[0].alias = new_alias
	conf2.write()

	conf1.update()
	assert conf1.deployments[0].alias == new_alias
	assert conf1.deployments[1].alias == depl.second["alias"]


def test_duplicate_alias(temp_repo: Callable):
	temp_repo(dupe_key="alias")
	errmsg = "duplicate alias values not allowed in public config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPublicConfig()


def test_duplicate_path(temp_repo: Callable):
	temp_repo(dupe_key="path")
	errmsg = "duplicate path values not allowed in public config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPublicConfig()


def test_duplicate_pubkey(temp_repo: Callable):
	temp_repo(dupe_key="pubkey")
	errmsg = "duplicate pubkey values not allowed in public config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPublicConfig()


def test_garbage_file_contents(temp_repo: Callable):
	temp_repo(garbage=True)
	with pytest.raises(orjson.JSONDecodeError):
		ProjectPublicConfig()
