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


from m2q_comm import createMessage


class Test_m2q_comm(unittest.TestCase):
    def test_createMessage_noWingMode(self):
        wingMode = False
        self.assertEqual(createMessage(0, 1, 0, wingMode), "1,0,0J")
        self.assertEqual(createMessage(1, 1, 1, wingMode), "1,1,L")

    def test_createMessage_yesWingMode(self):
        wingMode = True
        self.assertEqual(createMessage(0, 1, 0, wingMode), "11,0,0J")
        self.assertEqual(createMessage(1, 1, 1, wingMode), "11,1,L")

    def test_createMessage_messageType0(self):
        messageType = 0
        self.assertEqual(createMessage(messageType, 1, 0, False), "1,0,0J")

    def test_createMessage_messageType1(self):
        messageType = 1
        self.assertEqual(createMessage(messageType, 1, 0, False), "1,0,L")

    def test_createMessage_messageType2(self):
        messageType = 2
        self.assertEqual(createMessage(messageType, 1, 0, False), "\\<82>,0H")

    def test_createMessage_messageType3(self):
        messageType = 3
        self.assertEqual(createMessage(messageType, 1, 0, False), "\\<83>,0H")

    def test_createMessage_messageType4(self):
        messageType = 4
        self.assertEqual(createMessage(messageType, 1, 0, False), "\\<71>,2H")

    def test_createMessage_messageTypeOutOfValue(self):
        messageType = 5
        self.assertEqual(createMessage(messageType, 1, 0, False), None)
        messageType = -3
        self.assertEqual(createMessage(messageType, 1, 0, False), None)
        messageType = 9999
        self.assertEqual(createMessage(messageType, 1, 0, False), None)

    def test_createMessage_testGoodNoteValue(self):
        note = 10
        self.assertEqual(createMessage(0, 1, note, False), "1,10,0J")
        note = 123
        self.assertEqual(createMessage(0, 1, note, False), "1,123,0J")
        note = 8
        self.assertEqual(createMessage(0, 1, note, False), "1,8,0J")

    def test_createMessage_testNotGoodNoteValue(self):
        note = 135
        self.assertEqual(createMessage(0, 1, note, False), None)
        note = -3
        self.assertEqual(createMessage(0, 1, note, False), None)
        note = 9999
        self.assertEqual(createMessage(0, 1, note, False), None)

    def test_createMessage_testGoodChannelValue(self):
        channel = 10
        self.assertEqual(createMessage(0, channel, 10, False), "10,10,0J")
        channel = 6
        self.assertEqual(createMessage(0, channel, 10, False), "6,10,0J")

    def test_createMessage_testNotGoodChannelValue(self):
        channel = 16
        self.assertEqual(createMessage(0, channel, 10, False), None)
        channel = -3
        self.assertEqual(createMessage(0, channel, 10, False), None)
        channel = 9999
        self.assertEqual(createMessage(0, channel, 10, False), None)
