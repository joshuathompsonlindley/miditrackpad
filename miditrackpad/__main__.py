import logging

import click

from miditrackpad.midi import MidiManager

logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s]: %(message)s")


@click.command()
@click.option("--port", "-p", required=True, help="MIDI output port name")
@click.option(
    "--cc",
    "-c",
    default=1,
    help="MIDI Control Change number to send pressure data on (default: 1)",
)
def main(port: str, cc: int = 1) -> None:
    midi_manager: MidiManager = MidiManager(port, cc)

    try:
        midi_manager.start()
    except Exception:
        logging.info("Stopping MIDI manager.")
    finally:
        midi_manager.stop()


if __name__ == "__main__":
    main()
