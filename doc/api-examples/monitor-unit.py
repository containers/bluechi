#!/usr/bin/python3

import sys
import time
from dasbus.typing import get_native
from dasbus.loop import EventLoop
import dasbus.connection

def print_dict_changes(old, new):
    for key in sorted(set(old.keys()) | set(new.keys())):
        if key not in old:
            print(f" {key}: {new[key]}")
        elif key not in new:
            print(f" {key}: deleted")
        else:
            o = old[key]
            n = new[key]
            if o != n:
                print(f" {key}: {o} -> {n}")

if len(sys.argv) < 2:
    print("No unit name supplied")
    sys.exit(1)

unit_name = sys.argv[1]
node_name = "" # Match all

if len(sys.argv) > 2:
    node_name = sys.argv[2]

bus = dasbus.connection.SessionMessageBus()

manager = bus.get_proxy("org.containers.hirte",  "/org/containers/hirte")

monitor_path = manager.CreateMonitor()
monitor = bus.get_proxy("org.containers.hirte",  monitor_path)

old_values = {}

def unit_property_changed(node, unit, props):
    old_value = old_values.get(node, {})
    new_value = get_native(props)

    print(f"Unit {unit} on node {node} changed::")
    print_dict_changes(old_value, new_value)

    old_values[node] = new_value;

def unit_new(node, unit):
    print(f"New Unit {unit} on node {node}")

def unit_removed(node, unit):
    print(f"Removed Unit {unit} on node {node}")
    del old_values[node]

monitor.UnitPropertiesChanged.connect(unit_property_changed)
monitor.UnitNew.connect(unit_new)
monitor.UnitRemoved.connect(unit_removed)

monitor.Subscribe(node_name, unit_name);

if node_name == "":
    print(f"Waiting for changes to unit `{unit_name}` on any node");
else:
    print(f"Waiting for changes to unit `{unit_name}` on node '{node_name}'");

loop = EventLoop()
loop.run()
