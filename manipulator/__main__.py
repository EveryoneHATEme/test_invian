import sys

sys.path.append("/app")

import asyncio

from manipulator import Manipulator

if __name__ == "__main__":
    _manipulator = Manipulator()
    asyncio.run(_manipulator.listen_commands())
