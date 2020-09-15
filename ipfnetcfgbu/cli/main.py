from .root import cli

from .backup import cli_backup  # noqa
from .vcs import cli_vcs  # noqa


def run():
    cli(obj={})
