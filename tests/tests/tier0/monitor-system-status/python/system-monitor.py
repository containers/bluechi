# SPDX-License-Identifier: LGPL-2.1-or-later

from bluechi.api import Manager
from dasbus.loop import EventLoop
from dasbus.typing import Variant

import sys
import signal


def sig_handler(_signo, _stack_frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

try:
    f = open("/tmp/events", "w")

    def on_system_status_changed(status: Variant):
        con_status = status.get_string()
        f.write(f"{con_status},")
        f.flush()
        print(con_status)

    loop = EventLoop()

    mgr = Manager()
    mgr.on_status_changed(on_system_status_changed)

    loop.run()
finally:
    f.close()
