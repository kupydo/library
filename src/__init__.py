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
from kubernetes_asyncio import config
from models.namespace import Namespace
from client import ApiClient


async def main():
    ns = Namespace(name="asdfg")

    await config.load_kube_config()
    async with ApiClient() as api:
        resp = await api.delete(ns)
        print(vars(resp))


if __name__ == "__main__":
    asyncio.run(main())
