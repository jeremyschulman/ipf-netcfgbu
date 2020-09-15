import asyncio

import click
import maya


from aioipfabric.filters import parse_filter

from ipfnetcfgbu.config_model import ConfigModel
from ipfnetcfgbu.ipf import IPFabricClient
from ipfnetcfgbu import logging
from .root import cli, opt_config_file, WithConfigCommand


def exec_backup(config: ConfigModel):
    ipf_cfg = config.ipfabric

    log = logging.get_logger()

    log.info("Fetching inventory from IP Fabric")
    if ipf_cfg.filters:
        log.info(f"Using filter: {ipf_cfg.filters}")
        ipf_filters = parse_filter(ipf_cfg.filters)
    else:
        log.warning("No device filtering specified")
        ipf_filters = None

    ipf = IPFabricClient()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ipf.login())

    # obtain the device inventory that is matching the User provided filters.
    # This list of hostnames is used to filter the configuration files that are
    # requested.

    devices = loop.run_until_complete(
        ipf.fetch_devices(columns=["hostname"], filters=ipf_filters)
    )

    hostnames = {rec["hostname"] for rec in devices}

    def device_filter(hashrec):
        return hashrec["hostname"] in hostnames

    async def save_config(rec, config_text):
        hostname = rec["hostname"]
        print(f"GOT CONFIG: {hostname}")

    start_of_today = maya.now().snap("@d")
    since_ts = int(start_of_today.epoch * 1_000)

    print(f"Backup configs that have changed since: {start_of_today}")

    loop.run_until_complete(
        ipf.fetch_device_configs(
            since_ts=since_ts, on_config=save_config, device_filter=device_filter
        )
    )

    logging.stop()


@cli.command(name="backup", cls=WithConfigCommand)
@opt_config_file
@click.pass_context
def cli_backup(ctx, **_cli_opts):
    """
    Backup network configurations.
    """
    exec_backup(ctx.obj["config"])
