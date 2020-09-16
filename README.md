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