#!/usr/bin/env python
# SPDX-License-Identifier: MIT-0

from bluechi.api import Node

for unit in Node("my-node-name").list_units():
    # unit[name, description, ...]
    print(f"{unit[0]} - {unit[1]}")
