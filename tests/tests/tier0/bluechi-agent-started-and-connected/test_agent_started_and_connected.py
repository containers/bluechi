# SPDX-License-Identifier: LGPL-2.1-or-later

from typing import Dict

from bluechi_test.test import BluechiTest
from bluechi_test.machine import BluechiControllerMachine, BluechiAgentMachine
from bluechi_test.config import BluechiControllerConfig, BluechiAgentConfig


def foo_startup_verify(ctrl: BluechiControllerMachine, nodes: Dict[str, BluechiAgentMachine]):

    result, output = ctrl.bluechictl.get_status("node-foo", "bluechi-agent.service")
    assert result == 0
    assert str(output).split('\n')[2].split('|')[2].strip() == 'active'

    # TODO: Add code to test that agent on node foo is successfully connected to bluechi controller


def test_agent_foo_startup(
        bluechi_test: BluechiTest,
        bluechi_ctrl_default_config: BluechiControllerConfig,
        bluechi_node_default_config: BluechiAgentConfig):

    bluechi_node_default_config.node_name = "node-foo"
    bluechi_ctrl_default_config.allowed_node_names = [bluechi_node_default_config.node_name]

    bluechi_test.set_bluechi_controller_config(bluechi_ctrl_default_config)
    bluechi_test.add_bluechi_agent_config(bluechi_node_default_config)

    bluechi_test.run(foo_startup_verify)
