# Network Config Backup from IP Fabric to Github

As a User of the IP Fabric product, I want to copy the network device configuration from
IP Fabric into a Git repository.

This tool takes inspiration from the [netcfgbu](https://github.com/jeremyschulman/netcfgbu) project that backs up network configuration
using a direct SSH-to-device approach.

# Quick Start

Once you've configured your `ipfnetcfgbu.toml` configuration file, you can run the following
command to backup **all** devices, using "start of today" as the timestamp basis:

```shell
ipf-netcfgbu backup --force
```

To backup only those devices whose configurations have actually changed since "start of today":

```shell
ipf-netcfgbu backup
```

To save these configurations into your remote git repository:

```shell
ipf-netcfgbu vcs save
```

# Installation

This package is not yet in PyPi.  To install:

```sheel
pip install ipf-netcfgbu@git+https://github.com/jeremyschulman/ipf-netcfgbu.git
```
# Usage

```shell
Usage: ipf-netcfgbu [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  backup  Backup network configurations.
  vcs     Version Control System subcommands.
```

## Backup Command

The *backup* command provides the following options:

```shell
Usage: ipf-netcfgbu backup [OPTIONS]

  Backup network configurations.

Options:
  -C, --config FILENAME
  --start-date <DATE-TIME>  Identifies the starting timestamp date/time
  --end-date <DATE-TIME>    Identifies the ending timestamp date/time
  --force                   Force backup of all configs, not just those that
                            changed

  --dry-run                 Use to see device list that would be backed up
  --filters TEXT            Override the `filters` option in the config file
  --help                    Show this message and exit.
```

The `start-date` and `end-date` syntax follows values allowed by the Maya package.  For example
you can use expressions like "2 days ago" or explicit dates like "2020-sep-16".  You can
also provide a time with the date, for example "yesterday noon" or "2020-sep-16 2:30 pm"

The `filters` enables any IP Fabric allowable API filter; the expression syntax
is defined in the [aio-ipfabric](https://github.com/jeremyschulman/aio-ipfabric)
`filters` module.  Here are some examples:

```shell
# Hostname starts with "abc"

--filters 'hostname =~ "abc.*"'

# Site is "atl" or Hostname contains the substring "sw2"

--filters "or(site = atl, hostname has sw2)"

# Either:
#  (a) Site is "atl" and Hostname contains subscript "core"
#  (b) Site is "chc" and Hostname ends in "club-switch21" or "club-switch22"

--filters 'or(and(site = atl, hostname has core), and(site = chc, hostname =~ ".*club-switch2[12]"))'
```

More docs on that comming soon.  Ask for help via github issue if you need.

# Configuration File

The `ipf-netcfgbu` looks for a TOML based configuration file in one of the following places
   1.  As specified by the `-C` option
   2.  As specified by the `IPFNETCFGBU_CONFIGFILE` enviornment variable
   3.  $PWD/ipfnetcfgbu.toml

See Example: [ipfnetcfgbu.toml](ipfnetcfgbu.toml)<br/>

The configuration file has the following sections:

### defaults

   * `config_dir` - The local filesystem directory where the network
   configuration files will be stored after they are retrieved from IP Fabric.

### ipfabric

   * `credentials.username` - The IP Fabric login user-name
   * `credentials.password` - The IP Fabric login password
   * `credentials.token` - The IP Fabric authentication token

_NOTE_: Either the `token` or the (`username`, `password`) options must be provided.

   * `server_url` - The HTTPS URL to the IP Fabric system
   * `filters` - A string representing an IP Fabric filter expression used to limit the
   device records retrieved from IP Fabric that are used as the inventory for backup purposes.
   If no `filters` is provided, then all devices will be scoped for backup.
   * `strip_hostname_domains` - A list of string values that are domain-name suffix values you
   want to remove from the IP Fabric device stored hostname value.  In some device cases, NX-OS for example,
   the IP Fabric system stores the device FQDN.

### git

This is the same configuration structure as `netcfgbu`.<br/>
See [docs](https://github.com/jeremyschulman/netcfgbu/blob/master/docs/config-vcs-git.md) for details.

### loggers

This is the same configuration structure as `netcfgbu`.<br/>
See example [ipfnetcfgbu.toml](ipfnetcfgbu.toml) file for details.

# Environment Variables

   * `IPFNETCFGBU_CONFIGFILE` - filepath to your configuration file