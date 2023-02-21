% hirte-agent 1

## NAME

hirte-agent - Agent managing services on the local machine

## SYNOPSIS

**hirte-agent** [*options*]

## DESCRIPTION

Hirte is a service orchestrator tool intended for multi-node devices (e.g.: edge devices) clusters with a predefined number of nodes and with a focus on highly regulated environment such as those requiring functional safety (for example in cars).

A `hirte-agent` establishes a peer-to-peer connection to `hirte` and exposes its API to manage systemd units on it.

**hirte [OPTIONS]**

## OPTIONS

#### **--help**, **-h**

Print usage statement and exit.

#### **--host**, **-H**

The host used by `hirte-agent` to connect to `hirte`. Must be a valid IPv4 or IPv6. This option will overwrite the host defined in the configuration file.

#### **--port**, **-p**

The port on which `hirte` is listening for connection request and the `hirte-agent` is connecting to. This option will overwrite the port defined in the configuration file.

#### **--name**, **-n**

The unique name of this `hirte-agent` used for registering at `hirte`. This option will overwrite the port defined in the configuration file.

#### **--config**, **-c**

Path to the configuration file, see `hirte-agent.conf(5)`.

## Environment Variables

`hirte-agent` understands the following environment variables that can be used to override the settings from the configuration file (see `hirte-agent.conf(5)`).

#### **HIRTE_LOG_LEVEL**

The level used for logging. Supported values are:

- `DEBUG`
- `INFO`
- `WARN`
- `ERROR`

#### **HIRTE_LOG_TARGET**

The target where logs are written to. Supported values are:

- `stderr`
- `journald`

#### **HIRTE_LOG_IS_QUIET**

If this flag is set to `true`, no logs are written by hirte.

## Exit Codes

TBD

## CONFIGURATION FILES

TBD

## SEE ALSO

**[hirte-agent.conf(5)](https://github.com/containers/hirte/blob/main/doc/man/hirte-agent.conf.5.md)**
