#!/usr/bin/python3

import sys
from dasbus.typing import get_native
import dasbus.connection
bus = dasbus.connection.SessionMessageBus()

if len(sys.argv) != 3:
    print("No node name and unit supplied")
    sys.exit(1)

node_name = sys.argv[1]
unit_name = sys.argv[2]

manager = bus.get_proxy("org.containers.hirte",  "/org/containers/hirte")
node_path = manager.GetNode(node_name)
node = bus.get_proxy("org.containers.hirte",  node_path)

properties = node.GetUnitProperties(unit_name)
print(get_native(properties))
