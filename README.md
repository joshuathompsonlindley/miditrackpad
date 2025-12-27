# MIDI Trackpad Controller

Converts Mac trackpad pressure values to a virtual MIDI Control Change message. Uses Apple’s private MultitouchSupport framework, so it _might_ change on newer macOS versions. 

**Currently tested against a M1 Pro Macbook running macOS Tahoe 26.2**

## Requirements
- macOS with a Force Touch trackpad
- Python 3.11

## Installation and Usage
To install:
```bash
pip install -e .
```

To use, you can create and run a virtual MIDI port, which will start sending the pressure values to the specified CC at a rate of 60hz. The `--cc` value will default to 1, which is the Modulation Wheel:
```bash
python3 -m miditrackpad --port {PORT} --cc {CC}
```

Then select the your port as input in your DAW and arm a software instrument track.

### Choosing a different CC
Change `--cc` to another number (e.g., 11 for expression, 74 for filter cutoff). You can find a list of CC numbers and their use in the [MIDI 1 specification](https://midi.org/midi-1-0-control-change-messages).