import logging
import time
from typing import Any

import mido

from miditrackpad.multitouch import PressureManager


class MidiManager:
    def __init__(self, port: str, cc: int = 1) -> None:
        """Manages MIDI output based on trackpad pressure data."""
        self.port: str = port
        self.cc: int = cc
        self.output: Any = mido.open_output(port, virtual=True)
        self.pressure_manager: PressureManager = PressureManager()

        logging.info(f"MIDI output opened on port: {port}, CC number: {cc}")

        self.started: bool = False

    def __enter__(self) -> "MidiManager":
        return self

    def start(self) -> None:
        """Start the pressure manager and begin sending MIDI messages."""
        self.started = True

        with self.pressure_manager as pm:
            logging.info("Pressure manager started. Sending MIDI messages...")

            # Start sending MIDI messages at around 60hz
            while self.started:
                value_to_send: int = self.clamp_to_midi_range(pm.pressure())
                self.output.send(mido.Message("control_change", control=self.cc, value=value_to_send))
                logging.info(f"Sent MIDI CC {self.cc} {value_to_send}")
                time.sleep(1.0 / 60.0)

    def clamp_to_midi_range(self, pressure: float) -> int:
        """Map raw pressure (0..~1700) to MIDI 0-127 with a fixed deadzone."""

        # The amount of pressure that corresponds to max MIDI value (127)
        max_pressure: float = 1700.0
        # Deadzone to avoid noise at low pressure levels
        deadzone: float = 250.0

        # No point calculating if below deadzone
        if pressure <= deadzone:
            return 0

        # Normalize pressure to 0.0 - 1.0 range based on deadzone and max_pressure
        normalized: float = (pressure - deadzone) / (max_pressure - deadzone)

        # Scale to 0-127 and clamp to valid MIDI range
        scaled: int = int(normalized * 127)
        return max(0, min(127, scaled))

    def __exit__(self, exc_type: type | None, exc: BaseException | None, tb: object | None) -> None:
        """Stop sending MIDI messages."""
        self.started = False
        self.output.close()
