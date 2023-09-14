#!/usr/bin/env python
# SPDX-License-Identifier: MIT-0

from bluechi.api import Node

cpu_weight = Node("my-node-name").get_unit_property(
    "ldconfig.service", "org.freedesktop.systemd1.Service", "CPUWeight"
)
print(cpu_weight)
