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
            mock_MidiIn().get_ports.return_value = ['Fake midi']
            ports = probeMidiPorts()
            self.assertEqual(ports, ['Fake midi'])
