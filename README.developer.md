
# Hirte

- [Development](#development)
  - [Environment Setup](#environment-setup)
    - [Prerequisites](#prerequisites)
    - [Dependencies Installation](#dependencies-installation)
  - [Code Style](#code-style)
  - [Linting](#linting)
  - [Build](#build)
  - [Debug](#debug)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [Running](#running)
    - [hirte](#hirte)
    - [hirte-agent](#hirte-agent)
    - [hirtectl](#hirtectl)
- [Documentation](#documentation)
  - [Building MAN Pages](#building-man-pages)
- [Packaging](#packaging)

## Development

### Environment Setup

In order to develop the project you need to install following dependencies.

#### Prerequisites

To build the project on CentOS Stream 9 you need to enable CodeReady Build repository:

```bash
sudo dnf install dnf-plugin-config-manager
sudo dnf config-manager --set-enabled crb
sudo dnf install -y epel-release
```

#### Dependencies installation

```bash
sudo dnf install clang-tools-extra gcc make meson systemd-devel selinux-policy-devel
```

[markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) can be used for static analysis of markdown files.
Check the [installation guide](https://github.com/DavidAnson/markdownlint-cli2#install) and use the most appropriate way
of installation for your setup.

### Code Style

[clang-format](https://clang.llvm.org/docs/ClangFormat.html) is used to enforce a uniform code style. The formatting
of all source files can be checked via:

```bash
# only check for formatting
make check-fmt

# apply formatting to files 
make fmt
```

For the most part, this project follows systemd coding style:
[systemd-coding-style](https://github.com/systemd/systemd/blob/main/docs/CODING_STYLE.md). Also, this project borrows
some of the coding conventions from systemd. For example, function names pertaining to D-Bus services look like
`bus_service_set_property()`.

### Linting

[clang-tidy](https://clang.llvm.org/extra/clang-tidy/) is used for static analysis of C source codes.
[markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) is used for static analysis of markdown files.
[flake8](https://flake8.pycqa.org/en/latest/) is used for format checking and linting of python code.

The following make targets simplify the usage of the different linting tools:

```bash
# using clang-tidy, lint all C source files
make lint-c

# same as lint-c target, but auto-fix errors if possible
make lint-c-fix

# using markdownlint-cli2, lint all markdown files
make lint-markdown

# combines lint-c and lint-markdown
make lint
```

### Build

The project is using [meson](https://mesonbuild.com/) as its primary build system.

The binaries and other artifacts (such as the man pages) can be built via:

```bash
meson setup builddir
meson compile -C builddir
```

After successfully compiling the binaries, they can be installed into a destination directory (by default
`/usr/local/bin`) using:

```bash
meson install -C builddir
```

To install it into `builddir/bin` use:

```bash
meson install -C builddir --destdir bin
```

After building, the following binaries are available:

- `hirte`: the systemd service controller which is run on the main machine, sending commands to the agents and
  monitoring the progress
- `hirte-agent`: the node agent unit which connects with the controller and executes commands on the node machine
- `hirte-proxy`: an internally used application to resolve cross-node dependencies
- `hirtectl`: a helper (CLI) program to send an commands to the controller

#### Bindings

Bindings for the D-Bus API of `hirte` are located in [src/bindings](./src/bindings/). Please refer to the
[README.md](./src/bindings/README.md) for more details.

A complete set of typed python bindings for the D-Bus API is auto-generated. On any change to any of the [interfaces](./data/),
these need to be re-generated via

```bash
bash build-scripts/generate-bindings.sh python
```

### Debug

In some cases, developers might need a debug session with tools like gdb, here an example:

First, make sure **meson.build** contains **debug=true**.  

Rebuild the hirte project with debug symbols included:

```bash
hirte> make clean
hirte> meson install -C builddir --dest=bin
hirte> gdb --args ./builddir/bin/usr/local/bin/hirte -c /etc/hirte/hirte.conf
```

### Unit tests

Unit tests can be executed using following commands:

```bash
meson setup builddir
meson compile -C builddir
meson test -C builddir
```

or simply:

```bash
# unit tests
make test
# unit tests with valgrind
make test-with-valgrind
```

If you want to get coverage data you'll need `lcov` package installed:

```bash
# unit tests with coverage report
make test-coverage
# unit tests with valgrind and coverage report
make test-with-valgrind-coverage
```

will produce a coverage report in `builddir/meson-logs/coveragereport/index.html`

### Integration tests

All files related to the integration tests are located in [tests](./tests/) and are organized via
[tmt](https://tmt.readthedocs.io/en/stable/). How to get started with running and developing
integration tests for hirte is described in [tests/README](./tests/README.md).

### Running

The following sections describe how to run the built application(s) locally on one machine. For this, the assumed setup
used is described in the first section.

#### Assumed setup

The project has been build with the following command sequence:

```bash
meson setup builddir
meson compile -C builddir
meson install -C builddir --destdir bin
```

Meson will output the artifacts to `./builddir/bin/usr/local/`. This directory is referred to in the following sections
simply as `<builddir>`.

To allow `hirte` and `hirte-agent` to own a name on the local system D-Bus, the provided configuration
files need to be copied (if not already existing):

```bash
cp <builddir>/share/dbus-1/system.d/org.containers.hirte.Agent.conf /etc/dbus-1/system.d/
cp <builddir>/share/dbus-1/system.d/org.containers.hirte.conf /etc/dbus-1/system.d/
```

**Note:** Make sure to reload the dbus service so these changes take effect: `systemctl reload dbus-broker.service` (or
`systemctl reload dbus.service`)

#### hirte

The newly built controller can simply be run via `./<builddir>/bin/hirte`, but it is recommended to use a specific
configuration for development. This file can be passed in with the `-c` CLI option:

```bash
./<builddir>/bin/hirte -c <path-to-cfg-file>
```

#### hirte-agent

Before starting the agent, it is best to have the hirte controller already running. However, `hirte-agent` will
try to reconnect in the configured heartbeat interval.

Similar to `hirte`, it is recommended to use a dedicated configuration file for development:

```bash
./<builddir>/bin/hirte -c <path-to-cfg-file>
```

#### hirtectl

The newly built `hirtectl` can be used via:

```bash
./<builddir>/bin/hirtectl COMMANDS
```

## Documentation

Files for documentation of this project are located in the [doc](./doc/) directory comprising:

- [api examples](./doc/api-examples/): directory containing python files that use the D-Bus API of hirte, e.g. for starting
a systemd unit
- [man](./doc/man/): directory containing the markdown files for generating the man pages
(see [Building MAN pages](#building-man-pages) for more information)
- readthedocs files for building the documentation website of hirte (see [the README](./doc/README.md) for further information)
- [diagrams.drawio](./doc/diagrams.drawio) file containing all diagrams used for hirte

### Building MAN pages

The source markdown files for building the MAN pages are located in [doc/man](./doc/man/). For generating the MAN pages
from the markdown files [go-md2man](https://github.com/cpuguy83/go-md2man) is being used. Install it via:

```bash
sudo dnf install golang-github-cpuguy83-md2man
```

After executing a `meson install` the MAN pages are located in the `man/man*` directories.

## Packaging

Hirte is packaged as an RPM. The scripts used to create the SRPM and RPM may be found in [.build-scripts](./build-scripts).

The RPM creation [script](./build-scripts/build-rpm.sh) requires one environment variable:

- `ARTIFACTS_DIR` - full path to a directory where the RPMs will be saved.
  The script will create the directory if it does not exist

Please note that the RPM creation script also installs all build dependencies and therefore requires running with root privileges

In order to build an RPM locally use the following command:

```bash
sudo ARTIFACTS_DIR=${PWD}/output ./build-scripts/build-rpm.sh
```

Alternatively, by setting the environment variable `SKIP_BUILDDEP=yes`,
the installation process is skipped, allowing regular user permissions

```bash
SKIP_BUILDDEP=yes ARTIFACTS_DIR=${PWD}/output ./build-scripts/build-rpm.sh
```
