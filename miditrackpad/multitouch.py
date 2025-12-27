from ctypes import c_double, c_int
from typing import Any, Callable

from miditrackpad.types import (
    FrameCallback,
    MTDeviceCreateDefault,
    MTDeviceIsAvailable,
    MTDeviceRef,
    MTDeviceRelease,
    MTDeviceStart,
    MTDeviceStop,
    MTRegisterContactFrameCallback,
    MTUnregisterContactFrameCallback,
)


class PressureManager:
    def __init__(self) -> None:
        """Manages multitouch device to track pressure data."""
        self._multitouch_device: MTDeviceRef | None = None
        self._callback: Callable | None = None
        self.last_pressure: float = 0.0

    def __enter__(self) -> "PressureManager":
        # Ensure device is available
        if not MTDeviceIsAvailable():
            raise RuntimeError("Multitouch device not available")

        def on_frame(device: MTDeviceRef, touches: Any, count: c_int, timestamp: c_double, frame: c_int):
            # Update last pressure with the pressure of the last touch point
            self.last_pressure = touches[int(count) - 1].pressure if int(count) > 0 else 0.0

        # Register callback and start device
        self._callback = FrameCallback(on_frame)
        self._multitouch_device = MTDeviceCreateDefault()

        # Tell the OS to start sending touch data
        MTRegisterContactFrameCallback(self._multitouch_device, self._callback)
        MTDeviceStart(self._multitouch_device, 0)

        return self

    def __exit__(self, exc_type: type | None, exc: BaseException | None, tb: object | None) -> None:
        # Cleanup multitouch devices if registered
        if self._multitouch_device is not None:
            MTUnregisterContactFrameCallback(self._multitouch_device, self._callback)
            MTDeviceStop(self._multitouch_device)
            MTDeviceRelease(self._multitouch_device)

        self._multitouch_device = None
        self._callback = None

    def pressure(self) -> float:
        """Get the last reported pressure value."""
        return self.last_pressure
