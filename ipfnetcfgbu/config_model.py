import re
import os
from typing import Optional, List, Dict
from os.path import expandvars
from itertools import chain
from pathlib import Path

from pydantic import (
    BaseModel,
    SecretStr,
    BaseSettings,
    FilePath,
    validator,
    root_validator,
)


__all__ = [
    "ConfigModel",
    "Credentials",
    "GitSpec",
]

_var_re = re.compile(
    r"\${(?P<bname>[a-z0-9_]+)}" r"|" r"\$(?P<name>[^{][a-z_0-9]+)", flags=re.IGNORECASE
)


class NoExtraBaseModel(BaseModel):
    class Config:
        extra = "forbid"


class EnvExpand(str):
    """
    When a string value contains a reference to an environment variable, use
    this type to expand the contents of the variable using os.path.expandvars.

    For example like:
        password = "$MY_PASSWORD"
        foo_password = "${MY_PASSWORD}_foo"

    will be expanded, given MY_PASSWORD is set to 'boo!' in the environment:
        password -> "boo!"
        foo_password -> "boo!_foo"
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if found_vars := list(filter(len, chain.from_iterable(_var_re.findall(v)))):
            for var in found_vars:
                if (var_val := os.getenv(var)) is None:
                    raise ValueError(f'Environment variable "{var}" missing.')

                if not len(var_val):
                    raise ValueError(f'Environment variable "{var}" empty.')

            return expandvars(v)

        return v


class EnvSecretStr(EnvExpand, SecretStr):
    @classmethod
    def validate(cls, v):
        return SecretStr.validate(EnvExpand.validate(v))


class Credentials(NoExtraBaseModel):
    username: Optional[EnvExpand]
    password: Optional[EnvSecretStr]
    token: Optional[EnvSecretStr]

    @root_validator()
    def ensure_credentials(cls, values):
        if not any(
            (all((values.get("username"), values.get("password"))), values["token"])
        ):
            raise ValueError("Missing required credentials")
        return values


class Defaults(NoExtraBaseModel, BaseSettings):
    configs_dir: EnvExpand

    @validator("configs_dir")
    def _configs_dir(cls, value):  # noqa
        return Path(value).absolute()


class IPFabricModel(NoExtraBaseModel):
    server_url: EnvExpand
    credentials: Credentials
    filters: Optional[str]


class FilePathEnvExpand(FilePath):
    """ A FilePath field whose value can interpolated from env vars """

    @classmethod
    def __get_validators__(cls):
        yield from EnvExpand.__get_validators__()
        yield from FilePath.__get_validators__()


class GitSpec(NoExtraBaseModel):
    name: Optional[str]
    repo: str
    email: Optional[str]
    username: Optional[EnvExpand]
    password: Optional[EnvExpand]
    token: Optional[EnvSecretStr]
    deploy_key: Optional[FilePathEnvExpand]
    deploy_passphrase: Optional[EnvSecretStr]

    @validator("repo")
    def validate_repo(cls, repo):  # noqa
        expected = ("https:", "git@")
        if not repo.startswith(expected):
            raise ValueError(
                f"Bad repo URL [{repo}]: expected to start with {expected}."
            )
        return repo

    @root_validator
    def enure_proper_auth(cls, values):
        req = ("token", "deploy_key", "password")
        auth_vals = list(filter(None, (values.get(auth) for auth in req)))
        auth_c = len(auth_vals)
        if not auth_c:
            raise ValueError(
                f'Missing one of required auth method fields: {"|".join(req)}'
            )

        if auth_c > 1:
            raise ValueError(f'Only one of {"|".join(req)} allowed')

        if values.get("deploy_passphrase") and not values.get("deploy_key"):
            raise ValueError("deploy_key required when using deploy_passphrase")

        return values


class ConfigModel(NoExtraBaseModel):
    defaults: Defaults
    ipfabric: IPFabricModel
    git: Optional[List[GitSpec]]
    logging: Optional[Dict]
