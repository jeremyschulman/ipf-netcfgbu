from importlib import metadata
from pathlib import Path

import click
from first import first

from ipfnetcfgbu import config
from ipfnetcfgbu import consts

VERSION = metadata.version("ipf-netcfgbu")


# -----------------------------------------------------------------------------
#
#                           CLI Custom Click Commands
#
# -----------------------------------------------------------------------------


class WithConfigCommand(click.Command):
    def invoke(self, ctx):
        try:
            ctx.obj["config"] = config.load(fileio=ctx.params["config"])
            super().invoke(ctx)

        except Exception as exc:
            ctx.fail(str(exc))


def get_spec_nameorfirst(spec_list, spec_name=None):
    if not spec_list:
        return None

    if not spec_name:
        return first(spec_list)

    return first(spec for spec in spec_list if getattr(spec, "name", "") == spec_name)


# -----------------------------------------------------------------------------
#
#                                CLI Options
#
# -----------------------------------------------------------------------------


def check_for_default(ctx, opt, value):
    if value:
        return value

    if (fileobj := Path(consts.DEFAULT_CONFIG_FILE)).exists():
        return fileobj.open()

    ctx.fail("Missing configuration file")


opt_config_file = click.option(
    "-C",
    "--config",
    type=click.File(),
    callback=check_for_default,
)

# -----------------------------------------------------------------------------
# Inventory Options
# -----------------------------------------------------------------------------

opt_limits = click.option(
    "--limit",
    "-l",
    multiple=True,
    help="limit devices",
)

opt_excludes = click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="exclude devices",
)


# opt_batch = click.option(
#     "--batch",
#     "-b",
#     type=click.IntRange(1, 500),
#     help="inevntory record processing batch size",
# )


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass  # pragma: no cover
