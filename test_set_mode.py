import asyncio
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)

# Mocked FlightController
class MockFC:
    def __init__(self):
        self._connected = True
        
    async def get_telemetry(self):
        class T:
            flight_mode = "HOLD"
        return T()
        
    async def set_mode(self, mode: str) -> bool:
        if not self._connected:
            raise RuntimeError("Not connected")
        mode_upper = mode.upper()
        
        try:
            if mode_upper == "RTL":
                pass
            elif mode_upper == "LAND":
                pass
            elif mode_upper == "LOITER" or mode_upper == "HOLD":
                pass
            else:
                raise RuntimeError(f"Mode {mode} is not supported by the current flight-control interface.")
            
            # Verify mode change via telemetry
            for _ in range(1):
                await asyncio.sleep(0.1)
                t = await self.get_telemetry()
                if t.flight_mode and mode_upper in t.flight_mode.upper():
                    return True
                    
            return True
            
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise e
            raise RuntimeError(f"PX4 Set Mode failed: {e}")

# Mocked FlightManager
class MockFM:
    def __init__(self, fc):
        self.fc = fc
        
    async def set_mode(self, params: Dict[str, Any]) -> bool:
        mode = params.get('mode')
        success = await self.fc.set_mode(mode)
        return success

async def run():
    fc = MockFC()
    fm = MockFM(fc)
    
    modes = ["RTL", "STABILIZE", "GUIDED"]
    for m in modes:
        try:
            await fm.set_mode({"mode": m})
            print(f"{m}: Success")
        except RuntimeError as e:
            print(f"{m} Error caught correctly: {e}")

asyncio.run(run())
