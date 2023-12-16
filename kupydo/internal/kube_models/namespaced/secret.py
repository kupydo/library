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
from __future__ import annotations as anno
import orjson
import base64
from typing import Type
from dotmap import DotMap
from kubernetes_asyncio import client
from kupydo.internal.registry import *
from kupydo.internal.types import *
from kupydo.internal.base import *
from kupydo.internal import utils
from kupydo.internal import sec_ops


__all__ = [
    "BaseSecretValues",
    "BaseSecret",
    "OpaqueSecret",
    "BasicAuthSecret",
    "DockerSecret",
    "SSHSecret",
    "TLSSecret",
    "Secret"
]


class BaseSecretValues(KupydoBaseValues):
    data: OptionalDictStr
    string_data: OptionalDictStr
    immutable: OptionalBool
    subtype: OptionalStr


class BaseSecret(KupydoNamespacedModel):
    def __init__(self,
                 *,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 subtype: OptionalStr = None,
                 data: OptionalDictStr = None,
                 string_data: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            values=locals(),
            validator=BaseSecretValues
        )

    def _to_dict(self, new_values: DotMap = None) -> dict:
        v: BaseSecretValues = new_values or self._values
        return client.V1Secret(
            api_version="v1",
            kind="Secret",
            metadata=client.V1ObjectMeta(
                name=v.name,
                namespace=v.namespace,
                annotations=v.annotations,
                labels=v.labels
            ),
            data=v.data,
            string_data=v.string_data,
            immutable=v.immutable,
            type=v.subtype
        ).to_dict()

    def _api(self, session: client.ApiClient) -> KupydoApiActions:
        api = client.CoreV1Api(session)
        return KupydoApiActions(
            create=api.create_namespaced_secret,
            delete=api.delete_namespaced_secret,
            read=api.read_namespaced_secret,
            replace=api.replace_namespaced_secret,
            patch=api.patch_namespaced_secret
        )

    @staticmethod
    def _resolve_secret(keyword: str, value: str, from_file: bool = False) -> str:
        if enc_tag := sec_ops.unwrap_enc_tag(value):  # check if value is enc_tag
            secret = GlobalRegistry.get_secret(enc_tag)
            return secret.secret_value

        file_path, from_line = utils.first_external_caller()
        lines = utils.read_cached_file_lines(file_path)
        lineno = sec_ops.find_kwarg_line(lines, from_line, keyword, value)
        secret = utils.read_encode_rel_file(value) if from_file else value

        if GlobalRegistry.is_enabled():
            sfd = sec_ops.SecretFieldDetails(
                enc_tag=sec_ops.generate_enc_tag(),
                file_path=file_path,
                line_number=lineno,
                field_keyword=keyword,
                field_value=value,
                secret_value=secret,
                from_file=from_file
            )
            GlobalRegistry.register_secret(sfd)
        return secret


class OpaqueSecret(BaseSecret):
    def __init__(self,
                 *,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 immutable: OptionalBool = None,
                 string_data: OptionalDictStr = None
                 ) -> None:
        if string_data:
            for k, v in string_data.items():
                string_data[k] = self._resolve_secret(k, v)
        super().__init__(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels,
            immutable=immutable,
            subtype="Opaque",
            string_data=string_data
        )


class BasicAuthSecret(BaseSecret):
    def __init__(self,
                 *,
                 username: str,
                 password: str,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels,
            immutable=immutable,
            subtype="kubernetes.io/basic-auth",
            string_data=dict(
                username=self._resolve_secret("username", username),
                password=self._resolve_secret("password", password)
            )
        )


class DockerSecret(BaseSecret):
    def __init__(self,
                 *,
                 registry: str,
                 username: str,
                 password: str,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels,
            immutable=immutable,
            subtype="kubernetes.io/dockerconfigjson",
            data=self._create_dockerconfigjson(
                registry=self._resolve_secret("registry", registry),
                username=self._resolve_secret("username", username),
                password=self._resolve_secret("password", password)
            )
        )

    @staticmethod
    def _create_dockerconfigjson(registry: str, username: str, password: str) -> dict:
        auth_bytes = f"{username}:{password}".encode()
        auth_b64 = base64.b64encode(auth_bytes).decode()
        docker_config = {
            "auths": {
                registry: {
                    "username": username,
                    "password": password,
                    "auth": auth_b64
                }
            }
        }
        config_bytes = orjson.dumps(docker_config)
        config_b64 = base64.b64encode(config_bytes).decode()
        return {".dockerconfigjson": config_b64}


class SSHSecret(BaseSecret):
    def __init__(self,
                 *,
                 keyfile: str,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels,
            immutable=immutable,
            subtype="kubernetes.io/ssh-auth",
            data={
                "ssh-privatekey": self._resolve_secret(
                    "keyfile", keyfile, from_file=True)
            }
        )


class TLSSecret(BaseSecret):
    def __init__(self,
                 *,
                 certfile: str,
                 keyfile: str,
                 name: str,
                 namespace: OptionalStr = None,
                 annotations: OptionalDictStr = None,
                 labels: OptionalDictStr = None,
                 immutable: OptionalBool = None
                 ) -> None:
        super().__init__(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels,
            immutable=immutable,
            subtype="kubernetes.io/tls",
            data={
                "tls.crt": self._resolve_secret(
                    "certfile", certfile, from_file=True),
                "tls.key": self._resolve_secret(
                    "keyfile", keyfile, from_file=True)
            }
        )


class Secret:
    """
    A collection of BaseSecret subclasses.
    """
    BasicAuth: Type[BasicAuthSecret] = BasicAuthSecret
    Opaque: Type[OpaqueSecret] = OpaqueSecret
    Docker: Type[DockerSecret] = DockerSecret
    SSH: Type[SSHSecret] = SSHSecret
    TLS: Type[TLSSecret] = TLSSecret

    def __init__(self) -> None:
        """
        The Secret class cannot be instantiated, because it's a container\n
        for BaseSecret subclasses. Instead, use any of the subclasses with:\n
        Secret.Subclass(<any keyword args>)

        :raises SystemExit: Always
        """
        raise SystemExit(
            "KupydoError:\n"
            "The Secret class cannot be instantiated, because it's a container for BaseSecret subclasses."
            "Instead, use any of the subclasses with: Secret.Subclass(<any keyword args>)"
        )
