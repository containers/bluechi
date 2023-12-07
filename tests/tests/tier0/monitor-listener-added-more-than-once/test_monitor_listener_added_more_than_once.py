# SPDX-License-Identifier: LGPL-2.1-or-later

import os
from typing import Dict

from bluechi_test.test import BluechiTest
from bluechi_test.container import BluechiControllerContainer, BluechiNodeContainer
from bluechi_test.config import BluechiControllerConfig, BluechiNodeConfig


node_name_foo = "node-foo"
service_simple = "simple.service"


def exec(ctrl: BluechiControllerContainer, nodes: Dict[str, BluechiNodeContainer]):
    # copy prepared python scripts into container
    # will be run by not_added_as_peer.py script to create two processes with different bus ids
    ctrl.copy_container_script("create_monitor.py")
    ctrl.copy_container_script("listen.py")

    result, output = ctrl.run_python(os.path.join("python", "added_more_than_once.py"))
    if result != 0:
        raise Exception(output)


def test_monitor_listener_added_more_than_once(
        bluechi_test: BluechiTest,
        bluechi_ctrl_default_config: BluechiControllerConfig,
        bluechi_node_default_config: BluechiNodeConfig):

    config_node_foo = bluechi_node_default_config.deep_copy()
    config_node_foo.node_name = node_name_foo

    bluechi_ctrl_default_config.allowed_node_names = [node_name_foo]

    bluechi_test.set_bluechi_controller_config(bluechi_ctrl_default_config)
    bluechi_test.add_bluechi_node_config(config_node_foo)

    bluechi_test.run(exec)
