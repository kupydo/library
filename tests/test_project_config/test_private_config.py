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
from pytest_mock import MockerFixture
from typing import Callable, Literal
from kupydo.internal.project_config import *


@pytest.fixture(name="depl")
def fixture_depl() -> DotMap:
	return DotMap(
		first={
			'id': 'c5027735a24c3daa00fbc655b8aa20f3',
			'salt': 'p8Sn9cdqbuLvjaZaMMvAsBu0xtg0xBafBW4RarpDTCB5qjnVDnKlznDo452xPgUj',
			'part1': {
				'ciphertext': 'e03120dadf25b61bcec6c806beb0d0a256e9e83b',
				'nonce': '5d891767f3c07f742d68cad4f23415ac',
				'tag': '7bbda297e3fe856a49377b8254d85552'
			},
			'part2': {
				'ciphertext': 'c39d714762fb9cea101742c67db9b057a6863d5c',
				'nonce': 'd5612cf226da553fe5911c49026225aa',
				'tag': '49f5f3afe7ce216652a0d080d3b49afb'
			},
			'part3': {
				'ciphertext': '338822bbf405e93208b7b63abafa814000a20b42',
				'nonce': '2a0428d76cf0717946d78d902b26b817',
				'tag': '2e94e630493607f8d50b2f044e265597'
			}
		},
		second={
			'id': '7a1ed1611f32e46dae5890873eb9ea7c',
			'salt': 'RKLd8JaXMOTwTbj78PuamvgdFe8AzR1Ub5dCwCsF6FAzjK4Gij0sipT9PUdpZJRW',
			'part1': {
				'ciphertext': '0b30527babc20eca0869f7b3e6711aaac08c6602',
				'nonce': 'b730e6b1a0602ef3b32331d44e660e2e',
				'tag': 'ab81fb8debc8f89e6612f4496e95f691'
			},
			'part2': {
				'ciphertext': 'b38aebafc7922fcf9af5984814ac3b1b60b8a7fd',
				'nonce': 'b5bd85da174238fdc44652883779cfb0',
				'tag': 'fc0e5b7ed0eacabcbc6e684458c8a255'
			},
			'part3': {
				'ciphertext': '4b78b0246ccb1f82b306b438ad855ef0438aaef6',
				'nonce': '414f08f52a4e6cd72605dd192c3d9769',
				'tag': '04271be5d259eae70a072fad220fabac'
			}
		}
	)


@pytest.fixture(name="temp_repo")
def fixture_temp_repo(tmp_path: Path, depl: DotMap, mocker: MockerFixture) -> Callable:
	os.chdir(tmp_path)
	(tmp_path / ".git").mkdir()

	mocker.patch.object(Path, 'home', return_value=tmp_path)
	dkt = Literal["salt", "ciphertext", "nonce", "tag"]

	def custom_config_file(garbage: bool = False, dupe_key: dkt = None):
		config_path = ProjectPrivateConfig.get_config_path()
		with config_path.open("w") as file:
			if dupe_key == "salt":
				depl.second[dupe_key] = depl.first[dupe_key]
			elif dupe_key in ["ciphertext", "nonce", "tag"]:
				for part in ["part1", "part2", "part3"]:
					depl.second[part][dupe_key] = depl.first["part1"][dupe_key]

			file.write('{"deployments" : [error]}' if garbage else orjson.dumps({
				"deployments": [depl.first, depl.second]
			}).decode("utf-8"))

	return custom_config_file


def test_read_file_contents(temp_repo: Callable, depl: DotMap):
	temp_repo()
	conf = ProjectPrivateConfig()
	dump = conf.model_dump(warnings=False)
	for pd, fd in zip(dump["deployments"], depl.values()):
		for key in ["id", "salt"]:
			assert pd[key] == fd[key]
		for key1 in ["ciphertext", "nonce", "tag"]:
			for key2 in ["part1", "part2", "part3"]:
				assert pd[key2][key1] == fd[key2][key1]


def test_write_and_update(temp_repo: Callable, depl: DotMap):
	temp_repo()
	new_salt = 'a' * 64

	conf1 = ProjectPrivateConfig()
	assert conf1.deployments[0].salt == depl.first["salt"]
	assert conf1.deployments[1].salt == depl.second["salt"]

	conf2 = ProjectPrivateConfig()
	conf2.deployments[0].salt = new_salt
	conf2.write()

	conf1.update()
	assert conf1.deployments[0].salt == new_salt
	assert conf1.deployments[1].salt == depl.second["salt"]


def test_duplicate_salt(temp_repo: Callable):
	temp_repo(dupe_key="salt")
	errmsg = "duplicate salt values not allowed in private config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPrivateConfig()


def test_duplicate_ciphertext(temp_repo: Callable):
	temp_repo(dupe_key="ciphertext")
	errmsg = "duplicate ciphertext values not allowed in private config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPrivateConfig()


def test_duplicate_nonce(temp_repo: Callable):
	temp_repo(dupe_key="nonce")
	errmsg = "duplicate nonce values not allowed in private config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPrivateConfig()


def test_duplicate_tag(temp_repo: Callable):
	temp_repo(dupe_key="tag")
	errmsg = "duplicate tag values not allowed in private config file."
	with pytest.raises(ValueError, match=errmsg):
		ProjectPrivateConfig()


def test_garbage_file_contents(temp_repo: Callable):
	temp_repo(garbage=True)
	with pytest.raises(orjson.JSONDecodeError):
		ProjectPrivateConfig()
