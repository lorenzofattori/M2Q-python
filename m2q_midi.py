#   m2q_midi.py
#   Everything related the MIDI communication of m2q
#

import sys

from rtmidi.midiutil import open_midiinput

import m2q_comm

# global variables for midi handling
level = 0  # PB Level for Midi CC filtering
chan = 16  # midi channel received, from 1 to 16 for CC filtering


# Class MidiInputHandler - Revised version of the rtmidi example for non-polling midi handling
class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        # self._wallclock = time.time()

    def __call__(self, event, data=None):
        # second variable is deltatime, no idea what it means and why using it
        message, _ = event
        # self._wallclock += deltatime

        # message[0] is a combination of type of midi and channel
        # Example: 0x90 = note On - channel 1
        # 0x80 = note off - channel 1
        # 0x91 = note on - channel 2
        # 0xb0 = control change - channel 1
        # 0x9f = note on - channel 16
        # here I split them separately

        channel = (message[0] & 0x0F) + 1
        midiType = message[0] & 0xF0
        note = message[1]
        value = message[2]
        midiTypeDecode(channel, midiType, note, value)

        # print("[%s] %r" % (self.port, message))
        # print(
        #     f"Channel: {channel}, type: {hex(midiType)}, note: {note}, value: {value}"
        # )


# Midi setup - from the rtmidi example for non-polling midi handling
def midiSetup():
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

    return midiin


# decodes what type of midi message is sent and calls the proper handling function
def midiTypeDecode(channel, midiType, note, value):
    if midiType == 0x90:
        onNoteOn(channel, note, value)
    elif midiType == 0x80:
        onNoteOff(channel, note, value)
    elif midiType == 0xB0:
        onControlChange(channel, note, value)


""" 
Midi Handling Functions
"""
# handles note on (jumpToCue or activate cue stack triggering)
def onNoteOn(channel, note, velocity):
    if channel == 16:
        messageType = 2  # 2 = activate cuestack triggering

    else:
        messageType = 0  # 0 = jump to cue

    m2q_comm.createMessage(messageType, channel, note)


# handles note off (deactivate cue stack triggering)
def onNoteOff(channel, note, velocity):
    if channel == 16:
        messageType = 3  # 3 = de-activate cuestack triggering
        m2q_comm.createMessage(messageType, channel, note)


# handles control change (changes playback level)
def onControlChange(channel, control, value):
    messageType = 1  # 1 = jump to playback level
    # filtering on controller 1, other controller values are not used (this avoids that pressing stop in ableton resets playback)
    if control == 1:
        # only send messages if value is different, filter for reducing messages
        global level, chan  # no other way than using global?
        if value != level or channel != chan:
            level = value
            chan = channel
            m2q_comm.createMessage(messageType, chan, level)
