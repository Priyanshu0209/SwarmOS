import asyncio
from mavsdk import System
from mavsdk.mavlink_direct import MavlinkDirect

async def test():
    sys = System()
    print("Action has set_custom_mode?", hasattr(sys.action, 'set_custom_mode'))
    print("MavlinkDirect has send_message?", hasattr(sys.mavlink_direct, 'send_message'))

asyncio.run(test())
