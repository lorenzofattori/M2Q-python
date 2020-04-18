import unittest
from unittest.mock import patch

from m2q_midi import probe_midi_ports


class Test_M2Q_MIDI(unittest.TestCase):
    @patch("m2q_midi.MidiIn")
    def test_no_midi_interface(self, mock_MidiIn):
        mock_MidiIn().get_ports.return_value = []
        ports = probe_midi_ports()
        self.assertEqual(ports, [])

    @patch("m2q_midi.MidiIn")
    def test_single_midi_interface(self, mock_MidiIn):
        mock_MidiIn().get_ports.return_value = ["loopMIDI Port 1 1"]
        ports = probe_midi_ports()
        self.assertEqual(ports, ["loopMIDI Port 1"])


from m2q_comm import create_message


class Test_m2q_comm(unittest.TestCase):
    def test_create_message_noWingMode(self):
        wingMode = False
        self.assertEqual(create_message(0, 1, 0, wingMode), "1,0,0J")
        self.assertEqual(create_message(1, 1, 1, wingMode), "1,1,L")

    def test_create_message_yesWingMode(self):
        wingMode = True
        self.assertEqual(create_message(0, 1, 0, wingMode), "11,0,0J")
        self.assertEqual(create_message(1, 1, 1, wingMode), "11,1,L")

    def test_create_message_messageType0(self):
        messageType = 0
        self.assertEqual(create_message(messageType, 1, 0, False), "1,0,0J")

    def test_create_message_messageType1(self):
        messageType = 1
        self.assertEqual(create_message(messageType, 1, 0, False), "1,0,L")

    def test_create_message_messageType2(self):
        messageType = 2
        self.assertEqual(create_message(messageType, 1, 0, False), "\\<82>,0H")

    def test_create_message_messageType3(self):
        messageType = 3
        self.assertEqual(create_message(messageType, 1, 0, False), "\\<83>,0H")

    def test_create_message_messageType4(self):
        messageType = 4
        self.assertEqual(create_message(messageType, 1, 0, False), "\\<71>,2H")

    def test_create_message_messageTypeOutOfValue(self):
        messageType = 5
        self.assertEqual(create_message(messageType, 1, 0, False), None)
        messageType = -3
        self.assertEqual(create_message(messageType, 1, 0, False), None)
        messageType = 9999
        self.assertEqual(create_message(messageType, 1, 0, False), None)

    def test_create_message_testGoodNoteValue(self):
        note = 10
        self.assertEqual(create_message(0, 1, note, False), "1,10,0J")
        note = 123
        self.assertEqual(create_message(0, 1, note, False), "1,123,0J")
        note = 8
        self.assertEqual(create_message(0, 1, note, False), "1,8,0J")

    def test_create_message_testNotGoodNoteValue(self):
        note = 135
        self.assertEqual(create_message(0, 1, note, False), None)
        note = -3
        self.assertEqual(create_message(0, 1, note, False), None)
        note = 9999
        self.assertEqual(create_message(0, 1, note, False), None)

    def test_create_message_testGoodChannelValue(self):
        channel = 10
        self.assertEqual(create_message(0, channel, 10, False), "10,10,0J")
        channel = 6
        self.assertEqual(create_message(0, channel, 10, False), "6,10,0J")

    def test_create_message_testNotGoodChannelValue(self):
        channel = 16
        self.assertEqual(create_message(0, channel, 10, False), None)
        channel = -3
        self.assertEqual(create_message(0, channel, 10, False), None)
        channel = 9999
        self.assertEqual(create_message(0, channel, 10, False), None)
