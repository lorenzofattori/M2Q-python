import unittest
from unittest.mock import patch

from m2q_midi import probe_midi_ports
from m2q_comm import create_message


class TestM2QMidi(unittest.TestCase):
    @patch("m2q_midi.MidiIn")
    def test_no_midi_interface(self, mock_MidiIn): # pylint: disable=invalid-name
        mock_MidiIn().get_ports.return_value = []
        ports = probe_midi_ports()
        self.assertEqual(ports, [])

    @patch("m2q_midi.MidiIn")
    def test_single_midi_interface(self, mock_MidiIn): # pylint: disable=invalid-name
        mock_MidiIn().get_ports.return_value = ["loopMIDI Port 1 1"]
        ports = probe_midi_ports()
        self.assertEqual(ports, ["loopMIDI Port 1"])

class TestM2QComm(unittest.TestCase):
    def test_create_message_nowing_mode(self):
        wing_mode = False
        self.assertEqual(create_message(0, 1, 0, wing_mode), "1,0,0J")
        self.assertEqual(create_message(1, 1, 1, wing_mode), "1,1,L")

    def test_create_message_yeswing_mode(self):
        wing_mode = True
        self.assertEqual(create_message(0, 1, 0, wing_mode), "11,0,0J")
        self.assertEqual(create_message(1, 1, 1, wing_mode), "11,1,L")

    def test_create_message_message_type0(self):
        message_type = 0
        self.assertEqual(create_message(message_type, 1, 0, False), "1,0,0J")

    def test_create_message_message_type1(self):
        message_type = 1
        self.assertEqual(create_message(message_type, 1, 0, False), "1,0,L")

    def test_create_message_message_type2(self):
        message_type = 2
        self.assertEqual(create_message(message_type, 1, 0, False), "\\<82>,0H")

    def test_create_message_message_type3(self):
        message_type = 3
        self.assertEqual(create_message(message_type, 1, 0, False), "\\<83>,0H")

    def test_create_message_message_type4(self):
        message_type = 4
        self.assertEqual(create_message(message_type, 1, 0, False), "\\<71>,2H")

    def test_create_message_message_type_out_of_value(self):
        message_type = 5
        self.assertEqual(create_message(message_type, 1, 0, False), None)
        message_type = -3
        self.assertEqual(create_message(message_type, 1, 0, False), None)
        message_type = 9999
        self.assertEqual(create_message(message_type, 1, 0, False), None)

    def test_create_message_test_good_note_value(self):
        note = 10
        self.assertEqual(create_message(0, 1, note, False), "1,10,0J")
        note = 123
        self.assertEqual(create_message(0, 1, note, False), "1,123,0J")
        note = 8
        self.assertEqual(create_message(0, 1, note, False), "1,8,0J")

    def test_create_message_test_not_good_note_value(self):
        note = 135
        self.assertEqual(create_message(0, 1, note, False), None)
        note = -3
        self.assertEqual(create_message(0, 1, note, False), None)
        note = 9999
        self.assertEqual(create_message(0, 1, note, False), None)

    def test_create_message_test_good_channel_value(self):
        channel = 10
        self.assertEqual(create_message(0, channel, 10, False), "10,10,0J")
        channel = 6
        self.assertEqual(create_message(0, channel, 10, False), "6,10,0J")

    def test_create_message_test_not_good_channel_value(self):
        channel = 16
        self.assertEqual(create_message(0, channel, 10, False), None)
        channel = -3
        self.assertEqual(create_message(0, channel, 10, False), None)
        channel = 9999
        self.assertEqual(create_message(0, channel, 10, False), None)
