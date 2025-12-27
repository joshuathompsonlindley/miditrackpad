from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_bool,
    c_double,
    c_float,
    c_int,
    c_void_p,
)

# Might be different on different macOS versions!
MultitouchSupport = CDLL("/System/Library/PrivateFrameworks/MultitouchSupport.framework/MultitouchSupport")


class MTPoint(Structure):
    """Represents a multi-touch point in 2D space."""

    _fields_ = [("x", c_float), ("y", c_float)]


class MTVector(Structure):
    """Represents a multi-touch vector with position and velocity."""

    _fields_ = [("position", MTPoint), ("velocity", MTPoint)]


class MTTouch(Structure):
    """Represents a single touch event on the multi-touch device."""

    _fields_ = [
        ("frame", c_int),
        ("timestamp", c_double),
        ("identifier", c_int),
        ("state", c_int),
        ("fingerId", c_int),
        ("handId", c_int),
        ("normalizedPosition", MTVector),
        ("total", c_float),
        ("pressure", c_float),
        ("angle", c_float),
        ("majorAxis", c_float),
        ("minorAxis", c_float),
        ("absolutePosition", MTVector),
        ("field14", c_int),
        ("field15", c_int),
        ("density", c_float),
    ]


MTDeviceRef = c_void_p
"""Reference to a multi-touch device."""

FrameCallback = CFUNCTYPE(None, MTDeviceRef, POINTER(MTTouch), c_int, c_double, c_int)
"""Callback function type for handling multi-touch frames."""

# MTDeviceIsAvailable - Check if a multi-touch device is available
MTDeviceIsAvailable = MultitouchSupport.MTDeviceIsAvailable
MTDeviceIsAvailable.restype = c_bool

# MTDeviceCreateDefault - Create a reference to the default multi-touch device
MTDeviceCreateDefault = MultitouchSupport.MTDeviceCreateDefault
MTDeviceCreateDefault.restype = MTDeviceRef

# MTDeviceStart - Start receiving touch events from the multi-touch device
MTDeviceStart = MultitouchSupport.MTDeviceStart
MTDeviceStart.argtypes = [MTDeviceRef, c_int]

# MTDeviceStop - Stop receiving touch events from the multi-touch device
MTDeviceStop = MultitouchSupport.MTDeviceStop
MTDeviceStop.argtypes = [MTDeviceRef]

# MTDeviceRelease - Release the multi-touch device reference
MTDeviceRelease = MultitouchSupport.MTDeviceRelease
MTDeviceRelease.argtypes = [MTDeviceRef]

# MTRegisterContactFrameCallback - Register a callback for touch frames
MTRegisterContactFrameCallback = MultitouchSupport.MTRegisterContactFrameCallback
MTRegisterContactFrameCallback.argtypes = [MTDeviceRef, FrameCallback]

# MTUnregisterContactFrameCallback - Unregister a callback for touch frames
MTUnregisterContactFrameCallback = MultitouchSupport.MTUnregisterContactFrameCallback
MTUnregisterContactFrameCallback.argtypes = [MTDeviceRef, FrameCallback]
