#   m2q.py
#   THIS IS m2q in python
#   version 0.1
#   Date: 27/12/2019
#   Author: Lorenzo Fattori
#

# used libraries
import logging
import time
import sys

# UI stuff
import tkinter as tk
from tkinter import messagebox

# from PIL import ImageTk, Image

# other project files
import m2q_midi
import config
import m2q_comm
import m2q_ui


logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s", level=logging.WARNING
)


# Main Function
if __name__ == "__main__":

    # load settings on startup
    settings = config.loadSettings()

    # Create UI
    window = m2q_ui.createUi(settings)

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket)

    # handle shutdown when the windows X is pressed
    window.protocol("WM_DELETE_WINDOW", lambda: m2q_ui.shutdown(midiin, window))

    # everything is handled via the input callback, just refresh UI
    window.mainloop()

