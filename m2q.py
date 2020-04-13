#   m2q.py
#   This m2q in python
#   version 1.0
#   Date: 13/04/2019
#   Author: Lorenzo Fattori
#   More Info: https://github.com/lorenzofattori/M2Q
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

# import m2q_ui
from m2q_ui import UserInterface


logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s", level=logging.WARNING
)


# Main Function
if __name__ == "__main__":

    # load settings on startup
    settings = config.loadSettings()

    # Create UI
    # window = m2q_ui.createUi(settings)
    window = tk.Tk()
    userInterface = UserInterface(window, settings)

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])
    userInterface.udp_socket = udpSocket

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket, userInterface)
    userInterface.midi_interface = midiin

    # handle shutdown when the windows X is pressed
    # it will be nice to have this in the userinterface class, but I don't know how to properly handle the midiin port closing and deleting of midiin, any idea?
    window.protocol("WM_DELETE_WINDOW", lambda: userInterface.shutdown(midiin))

    # everything is handled via the input callback, just refresh UI
    window.mainloop()
