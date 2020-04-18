#   m2q_midi.py
#   Everything related the MIDI communication of m2q
#

import logging

# used for getting midi ports
from rtmidi import (
    API_LINUX_ALSA,
    API_MACOSX_CORE,
    API_RTMIDI_DUMMY,
    API_UNIX_JACK,
    API_WINDOWS_MM,
    MidiIn,
    get_compiled_api,
    midiutil,
)

import m2q_comm

# Class MidiInputHandler - Revised version of the rtmidi example for non-polling midi handling
class MidiInputHandler:
    def __init__(self, settings, udp_socket, user_interface):
        # self._wallclock = time.time()
        self.settings = settings
        self.udp_socket = udp_socket
        self.level = 0  # PB Level for Midi CC filtering
        self.chan = 16  # midi channel received, from 1 to 16 for CC filtering
        self.beatcounter = 0  # used for counting tap to tempo
        self.user_interface = user_interface

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

        logging.debug("MidiInputHandler __call__: %s", str(message))

        channel = None
        note = None

        midi_type = message[0]

        # handling midiClock, does not have message[1] and [2]
        if midi_type in (0xFA, 0xFB, 0xFC, 0xF8):
            pass

        # handling noteOn, noteOff and controlChange
        elif (
                (message[0] & 0xF0) == 0x90
                or (message[0] & 0xF0) == 0x80
                or (message[0] & 0xF0) == 0xB0
        ):
            # in this case message[0] contains both the type and the channel, I need to split them
            channel = (message[0] & 0x0F) + 1
            midi_type = message[0] & 0xF0
            note = message[1]
            value = message[2]

            # flash MIDIIN led
            self.user_interface.flash("MIDI")

        else:
            logging.debug("Incoming midi type not supported")
            return

        # decodes what type of midi message is sent and calls the proper handling function
        remote_message = None

        if midi_type == 0x90:
            if self.settings["cueStackMode"]:
                # handles note on (jumpToCue or activate cue stack triggering)
                if channel == 16:
                    # 2 = activate cuestack triggering
                    remote_message = m2q_comm.create_message(2, channel, note, None)
                else:
                    if self.settings["jumpMode"]:
                        # 0 = jump to cue
                        remote_message = m2q_comm.create_message(
                            0, channel, note, self.settings["wingMode"]
                        )

        elif midi_type == 0x80:
            # handles note off (deactivate cue stack triggering)
            if channel == 16:
                if self.settings["cueStackMode"]:
                    # 3 = de-activate cuestack triggering
                    remote_message = m2q_comm.create_message(3, channel, note, None)

        elif midi_type == 0xB0:
            # handles control change (changes playback level)
            if self.settings["levelMode"]:
                # filtering on controller 1, other controller values are not used
                # (this avoids that pressing stop in ableton resets playback)
                if note == 1:
                    # only send messages if value is different, filter for reducing messages
                    if channel != 16:
                        # ch 16 only for cue stack, no level
                        if value != self.level or channel != self.chan:
                            # save current values for next check
                            self.level = value
                            self.chan = channel

                            remote_message = m2q_comm.create_message(
                                1, channel, value, self.settings["wingMode"]
                            )

        elif midi_type in (0xFA, 0xFB, 0xFC, 0xF8):
            # handles clock start/stop etc
            if self.settings["tapToTempoMode"]:
                self.beatcounter += 1
                if self.beatcounter == 24:
                    self.beatcounter = 0
                    remote_message = m2q_comm.create_message(4, channel, note, None)

        if remote_message is not None:
            # Send the UDP message
            m2q_comm.send_udp(
                self.udp_socket,
                remote_message,
                self.settings["destinationIP"],
                self.settings["destPort"],
                self.user_interface,
            )


def probe_midi_ports():
    apis = {
        API_MACOSX_CORE: "macOS (OS X) CoreMIDI",
        API_LINUX_ALSA: "Linux ALSA",
        API_UNIX_JACK: "Jack Client",
        API_WINDOWS_MM: "Windows MultiMedia",
        API_RTMIDI_DUMMY: "RtMidi Dummy",
    }

    available_apis = get_compiled_api()

    for api, _ in sorted(apis.items()):
        if api in available_apis:
            try:
                midi = MidiIn(api)
                ports = midi.get_ports()
            except SystemError as exc:
                logging.warning("Could not probe MIDI input ports: %s", exc)
                return []

            del midi

            if not ports:
                return []

            # get_ports returns a list of ports in the order of the ports.
            # The port name contains the port number we don't want so let's strip it away
            renamed_ports = []
            for index, port in enumerate(ports):
                port = port[: -(len(str(index)) + 1)]
                renamed_ports.append(port)
            return renamed_ports


def activate_midi_port(user_interface, selected_port):
    midiin, port_name = midiutil.open_midiinput(selected_port)
    ui_set_midi_port(user_interface, selected_port)

    return midiin, port_name


def change_midi_port(user_interface, new_port_index, settings):
    user_interface.midi_interface.close_port()
    user_interface.midi_interface.open_port(new_port_index)
    user_interface.midi_interface.set_callback(
        MidiInputHandler(settings, user_interface.udp_socket, user_interface)
    )


def ui_set_midi_ports_choices(user_interface, ports):
    for _, name in enumerate(ports):
        if name not in user_interface.interfaces_value["values"]:
            user_interface.interfaces_value["values"] = (
                *user_interface.interfaces_value["values"],
                name,
            )


def ui_set_midi_port(user_interface, port):
    user_interface.interfaces_value.set(port)

def get_midi_interfaces():
    ports = probe_midi_ports()

    # Todo: What should be done when there is no ports available?
    if not ports:
        return []

    return ports

def refresh_midi_interfaces(user_interface, tk_root):
    ports = get_midi_interfaces()
    ui_set_midi_ports_choices(user_interface, ports)
    tk_root.after(5000, refresh_midi_interfaces, user_interface, tk_root)

# Midi setup - from the rtmidi example for non-polling midi handling
def midi_setup(settings, udp_socket, user_interface):
    ports = get_midi_interfaces()
    ui_set_midi_ports_choices(user_interface, ports)

    try:
        if settings["interface"] in ports:
            selected_port = settings["interface"]
        else:
            selected_port = ports[0]
    except KeyError:
        selected_port = ports[0]

    midiin, _ = activate_midi_port(user_interface, selected_port)

    logging.debug("Attaching MIDI input callback handler.")
    midiin.ignore_types(timing=False)
    midiin.set_callback(MidiInputHandler(settings, udp_socket, user_interface))

    return midiin
