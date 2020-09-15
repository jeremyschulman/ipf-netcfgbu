from .root import cli

# from .backup import cli_backup
from .vcs import cli_vcs  # noqa


def run():
    cli(obj={})
