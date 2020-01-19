#   m2q_midi.py
#   Everything related the MIDI communication of m2q
#

import sys
import logging

from rtmidi.midiutil import open_midiinput

import m2q_comm


# Class MidiInputHandler - Revised version of the rtmidi example for non-polling midi handling
class MidiInputHandler(object):
    def __init__(self, port, settings, udpSocket):
        self.port = port
        # self._wallclock = time.time()
        self.settings = settings
        self.udpSocket = udpSocket
        self.level = 0  # PB Level for Midi CC filtering
        self.chan = 16  # midi channel received, from 1 to 16 for CC filtering
        self.beatcounter = 0  # used for counting tap to tempo

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

        logging.debug("MidiInputHandler __call__: " + str(message))

        channel = None
        note = None

        midiType = message[0]

        # handling midiClock, does not have message[1] and [2]
        if midiType == 0xFA or midiType == 0xFB or midiType == 0xFC or midiType == 0xF8:
            pass

        # handling noteOn, noteOff and controlChange
        elif (
            (message[0] & 0xF0) == 0x90
            or (message[0] & 0xF0) == 0x80
            or (message[0] & 0xF0) == 0xB0
        ):
            # in this case message[0] contains both the type and the channel, I need to split them
            channel = (message[0] & 0x0F) + 1
            midiType = message[0] & 0xF0
            note = message[1]
            value = message[2]

        else:
            logging.debug("Incoming midi type not supported")
            return

        # decodes what type of midi message is sent and calls the proper handling function
        remoteMessage = None

        if midiType == 0x90:
            if self.settings["cueStackMode"] == True:
                # handles note on (jumpToCue or activate cue stack triggering)
                if channel == 16:
                    # 2 = activate cuestack triggering
                    remoteMessage = m2q_comm.createMessage(2, channel, note, None)
                else:
                    if self.settings["jumpMode"] == True:
                        # 0 = jump to cue
                        remoteMessage = m2q_comm.createMessage(
                            0, channel, note, self.settings["wingMode"]
                        )

        elif midiType == 0x80:
            # handles note off (deactivate cue stack triggering)
            if channel == 16:
                # 3 = de-activate cuestack triggering
                remoteMessage = m2q_comm.createMessage(3, channel, note, None)

        elif midiType == 0xB0:
            # handles control change (changes playback level)
            if self.settings["levelMode"] == True:
                # filtering on controller 1, other controller values are not used (this avoids that pressing stop in ableton resets playback)
                if note == 1:
                    # only send messages if value is different, filter for reducing messages
                    if channel != 16:
                    #ch 16 only for cue stack, no level
                        if value != self.level or channel != self.chan:
                            # save current values for next check
                            self.level = value
                            self.chan = channel

                            remoteMessage = m2q_comm.createMessage(
                                1, channel, value, self.settings["wingMode"]
                            )

        elif (
            midiType == 0xFA or midiType == 0xFB or midiType == 0xFC or midiType == 0xF8
        ):
            # handles clock start/stop etc
            if self.settings["tapToTempoMode"] == True:
                self.beatcounter += 1
                if self.beatcounter == 24:
                    self.beatcounter = 0
                    remoteMessage = m2q_comm.createMessage(4, channel, note, None)

        if remoteMessage != None:
            # Send the UDP message
            m2q_comm.sendUdp(
                self.udpSocket,
                remoteMessage,
                self.settings["destinationIP"],
                self.settings["destPort"],
            )


# Midi setup - from the rtmidi example for non-polling midi handling
def midiSetup(settings, udpSocket):
    # Prompts user for MIDI input port, unless a valid port number or name
    # is given as the first argument on the command line.
    # API backend defaults to ALSA on Linux.
    port = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.ignore_types(timing=False)
    midiin.set_callback(MidiInputHandler(port_name, settings, udpSocket))

    return midiin

