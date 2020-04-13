import unittest
from unittest.mock import patch

from m2q_midi import probeMidiPorts


class Test_M2Q_MIDI(unittest.TestCase):
    @patch("m2q_midi.MidiIn")
    def test_no_midi_interface(self, mock_MidiIn):
        mock_MidiIn().get_ports.return_value = []
        ports = probeMidiPorts()
        self.assertEqual(ports, [])

    @patch("m2q_midi.MidiIn")
    def test_single_midi_interface(self, mock_MidiIn):
        mock_MidiIn().get_ports.return_value = ["loopMIDI Port 1 1"]
        ports = probeMidiPorts()
        self.assertEqual(ports, ["loopMIDI Port 1"])


class Test_m2q_comm(unittest.TestCase):
    def test_createMessage(self):
        pass
