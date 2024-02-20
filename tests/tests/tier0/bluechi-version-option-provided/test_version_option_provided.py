# SPDX-License-Identifier: LGPL-2.1-or-later

from typing import Dict

from bluechi_test.test import BluechiTest
from bluechi_test.machine import BluechiControllerMachine, BluechiAgentMachine
from bluechi_test.config import BluechiControllerConfig


def check_help_option(ctrl: BluechiControllerMachine, _: Dict[str, BluechiAgentMachine]):
    rpm_re, rpm_out = ctrl.exec_run('rpm -q --qf "%{version}-%{release}" bluechi-controller')
    assert rpm_re == 0

    # There is no way to strip dist part from the release using rpm query flags, so we need to replace it manually
    bc_ver_rel = rpm_out.replace(".el9", "")
    executables = [
        '/usr/libexec/bluechi-controller',
        '/usr/libexec/bluechi-agent'
    ]

    for executable in executables:
        s_re, s_out = ctrl.exec_run(f"{executable} -v")
        l_re, l_out = ctrl.exec_run(f"{executable} --version")

        assert s_re == 0
        assert l_re == 0
        assert s_out == l_out
        assert bc_ver_rel in s_out


def test_version_option_provided(bluechi_test: BluechiTest, bluechi_ctrl_default_config: BluechiControllerConfig):
    bluechi_test.set_bluechi_controller_config(bluechi_ctrl_default_config)

    bluechi_test.run(check_help_option)
