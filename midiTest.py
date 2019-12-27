#
# midiin_callback.py
#
"""Show how to receive MIDI input by setting a callback function."""


import logging
import sys

import time

from rtmidi.midiutil import open_midiinput

# log = logging.getLogger("midiin_callback")
# logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        # self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        # self._wallclock += deltatime

        # message[0] is a combination of type of midi and channel
        # Example: 0x90 = note On - channel 1
        # 0x80 = note off - channel 1
        # 0x91 = note on - channel 2
        # 0xb0 = control change - channel 1
        # 0x9f = note on - channel 16
        # here I split them separately

        # WARNING - channel goes from 0 to 15 not from 1 to 16!
        channel = message[0] & 0x0F
        # this is in decimal, if you want to print 0x80 you need to convert it in hex
        midiType = message[0] & 0xF0
        note = message[1]
        value = message[2]

        print("[%s] %r" % (self.port, message))
        print(
            f"Channel: {channel}, type: {hex(midiType)}, note: {note}, value: {value}"
        )


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("")
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
