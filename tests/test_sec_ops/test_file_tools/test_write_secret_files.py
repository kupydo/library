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
import orjson
from pathlib import Path
from kupydo.internal import utils
from kupydo.internal import sec_ops


def test_with_valid_data(mocker, tmp_path):
	heart_path = Path("C:/projects/myapp/clusters/staging/Heart.py")
	rel_path = 'clusters/staging/Heart.py'
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
	mocked_rel_path = mocker.patch.object(
		target=utils,
		attribute='repo_abs_to_rel_path',
		return_value=rel_path
	)
	sec_ops.write_secret_store_files(tmp_path, sfd_list)
	mocked_rel_path.assert_called_once_with(heart_path)

	secret_file = tmp_path / "id1"
	assert secret_file.exists()

	with secret_file.open('rb') as file:
		data = orjson.loads(file.read())
		assert data["file_path"] == rel_path
		assert data["enc_tag"] == "id1"


def test_with_empty_list(tmp_path):
	sec_ops.write_secret_store_files(tmp_path, [])
	assert not any(tmp_path.iterdir())
