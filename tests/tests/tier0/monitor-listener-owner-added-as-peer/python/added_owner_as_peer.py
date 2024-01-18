# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from bluechi.api import Controller, Monitor
from dasbus.error import DBusError

node = "node-foo"
service = "simple.service"


class TestListenerAddedIsOwner(unittest.TestCase):

    def test_listener_added_is_owner(self):

        mgr = Controller()
        monitor_path = mgr.create_monitor()
        monitor = Monitor(monitor_path)

        with self.assertRaises(DBusError):
            monitor.add_peer(mgr.bus.connection.get_unique_name())


if __name__ == "__main__":
    unittest.main()
