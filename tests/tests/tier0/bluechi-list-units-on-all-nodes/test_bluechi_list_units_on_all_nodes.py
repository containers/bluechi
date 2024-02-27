# SPDX-License-Identifier: LGPL-2.1-or-later

import re

from typing import Dict, Tuple

from bluechi_test.config import BluechiControllerConfig, BluechiAgentConfig
from bluechi_test.machine import BluechiControllerMachine, BluechiAgentMachine
from bluechi_test.test import BluechiTest


node_foo_name = "node-foo"
node_bar_name = "node-bar"


def parse_bluechictl_output(output: str) -> Dict[str, Dict[str, Tuple[str, str]]]:
    line_pat = re.compile(r"""\s*(?P<node_name>[\S]+)\s*\|
                              \s*(?P<unit_name>[\S]+)\s*\|
                              \s*(?P<state>[\S]+)\s*\|
                              \s*(?P<sub_state>[\S]+)\s*""",
                          re.VERBOSE)
    result = {}
    for line in output.splitlines():
        if line.startswith("NODE ") or line.startswith("===="):
            # Ignore header lines
            continue

        match = line_pat.match(line)
        if not match:
            raise Exception(f"Error parsing bluechictl list-units output, invalid line: '{line}'")

        node_units = result.get(match.group("node_name"))
        if not node_units:
            node_units = {}
            result[match.group("node_name")] = node_units

        if match.group("unit_name") in node_units:
            raise Exception(f"Error parsing bluechictl list-units output, unit already reported, line: '{line}'")

        node_units[match.group("unit_name")] = (match.group("state"), match.group("sub_state"))

    return result


def verify_units(all_units: Dict[str, Tuple[str, str]], output: str, node_name: str):
    esc_seq = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    line_pat = re.compile(r"""\s*(?P<unit_name>\S+)
                              .*loaded
                              \s+(?P<state>\S+)
                              \s+(?P<sub_state>\S+)
                              \s+.*$
                          """,
                          re.VERBOSE)
    for line in output.splitlines():
        # Some systemctl output contains ANSI sequences, which we need to remove before matching
        line = esc_seq.sub('', line)

        match = line_pat.match(line)
        if not match:
            raise Exception(f"Error parsing systemctl list-units output, invalid line: '{line}'")

        found = all_units.get(match.group("unit_name"))
        if not found or match.group("state") != found[0] or match.group("sub_state") != found[1]:
            raise Exception("Unit '{}' with state '{}' and substate '{}' reported by systemctl"
                            " on node '{}', but not reported by bluechictl".format(
                                match.group("unit_name"),
                                match.group("state"),
                                match.group("sub_state"),
                                node_name))


def exec(ctrl: BluechiControllerMachine, nodes: Dict[str, BluechiAgentMachine]):
    node_foo = nodes[node_foo_name]
    node_bar = nodes[node_bar_name]

    all_res, all_out = ctrl.bluechictl.list_units()
    assert all_res == 0
    all_units = parse_bluechictl_output(all_out)

    foo_res, foo_out = node_foo.systemctl.list_units()
    assert foo_res == 0
    verify_units(all_units[node_foo_name], foo_out, node_foo_name)

    bar_res, bar_out = node_bar.systemctl.list_units()
    assert bar_res == 0
    verify_units(all_units[node_bar_name], bar_out, node_bar_name)


def test_bluechi_nodes_statuses(
        bluechi_test: BluechiTest,
        bluechi_ctrl_default_config: BluechiControllerConfig,
        bluechi_node_default_config: BluechiAgentConfig):

    node_foo_cfg = bluechi_node_default_config.deep_copy()
    node_foo_cfg.node_name = node_foo_name

    node_bar_cfg = bluechi_node_default_config.deep_copy()
    node_bar_cfg.node_name = node_bar_name

    bluechi_ctrl_default_config.allowed_node_names = [node_foo_name, node_bar_name]

    bluechi_test.set_bluechi_controller_config(bluechi_ctrl_default_config)
    bluechi_test.add_bluechi_agent_config(node_foo_cfg)
    bluechi_test.add_bluechi_agent_config(node_bar_cfg)

    bluechi_test.run(exec)
