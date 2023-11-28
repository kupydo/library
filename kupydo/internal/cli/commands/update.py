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
import asyncio
from typer import Typer


update_app = Typer(name="update")


# async def main():
# 	tasks = list()
# 	for tool in [CryptoTool.SOPS, CryptoTool.AGE]:
# 		coro = fetch_latest_release(tool)
# 		task = asyncio.create_task(coro)
# 		tasks.append(task)
# 	releases = await asyncio.gather(*tasks)
#
# 	tasks = list()
# 	for rel in releases:
# 		coro = download_compatible_asset(rel)
# 		task = asyncio.create_task(coro)
# 		tasks.append(task)
# 	paths = await asyncio.gather(*tasks)
#
# 	for rel, path in zip(releases, paths):
# 		install_asset(rel.tool, path)
#
# 	update_status_file(releases)
#
# sf = StatusFile.read()
# 	for k in sf.keys():
# 		if k == 'comment':
# 			continue
# 		sf[k] = DotMap(
# 			last_update='',
# 			current_version=''
# 		)
#
# @init_app.callback(invoke_without_command=True)
# def cmd_decrypt():
# 	asyncio.run(main())
