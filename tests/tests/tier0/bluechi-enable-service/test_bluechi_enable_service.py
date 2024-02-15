# SPDX-License-Identifier: LGPL-2.1-or-later

import os
from typing import Dict

from bluechi_test.config import BluechiControllerConfig, BluechiAgentConfig
from bluechi_test.machine import BluechiControllerMachine, BluechiAgentMachine
from bluechi_test.test import BluechiTest


node_foo_name = "node-foo"
simple_service = "simple.service"


def exec(ctrl: BluechiControllerMachine, nodes: Dict[str, BluechiAgentMachine]):
    foo = nodes[node_foo_name]

    source_dir = "systemd"
    target_dir = os.path.join("/", "etc", "systemd", "system")

    foo.copy_systemd_service(simple_service, source_dir, target_dir)
    assert foo.wait_for_unit_state_to_be(simple_service, "inactive")

    if not foo.systemctl.is_unit_disabled(simple_service, check_result=False):
        raise Exception(f"Failed pre-check if unit {simple_service} is disabled")

    ctrl.bluechictl.enable_unit(node_foo_name, simple_service)

    if not foo.systemctl.is_unit_enabled(simple_service, check_result=False):
        raise Exception(f"Unit {simple_service} expected to be enabled, but is not")


def test_proxy_service_start(
        bluechi_test: BluechiTest,
        bluechi_ctrl_default_config: BluechiControllerConfig,
        bluechi_node_default_config: BluechiAgentConfig):

    node_foo_cfg = bluechi_node_default_config.deep_copy()
    node_foo_cfg.node_name = node_foo_name

    bluechi_ctrl_default_config.allowed_node_names = [node_foo_name]

    bluechi_test.set_bluechi_controller_config(bluechi_ctrl_default_config)
    bluechi_test.add_bluechi_agent_config(node_foo_cfg)

    bluechi_test.run(exec)
