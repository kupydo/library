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
import orjson
from kupydo.internal import sec_ops


def test_with_valid_data(tmp_path):
	os.chdir(tmp_path)
	(tmp_path / ".git").mkdir()
	heart_path = tmp_path / "Heart.py"
	sfd_list = [
		sec_ops.SecretFieldDetails(
			enc_tag="id1",
			file_path=heart_path,
			line_number=1,
			field_keyword="key",
			field_value="value",
			secret_value="secret",
			from_file=False
		)
	]
	sec_ops.write_secret_store_files(tmp_path, sfd_list)
	secret_file = tmp_path / "id1"
	assert secret_file.exists()

	with secret_file.open('rb') as file:
		data = orjson.loads(file.read())

	sfd = sec_ops.SecretFieldDetails(**data)
	assert sfd.file_path == heart_path
	assert sfd.secret_value == "secret"
	assert sfd.enc_tag == "id1"


def test_with_empty_list(tmp_path):
	sec_ops.write_secret_store_files(tmp_path, [])
	assert not any(tmp_path.iterdir())
