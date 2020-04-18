'''
    m2q.py
    This m2q in python
    version 1.0
    Date: 13/04/2019
    Author: Lorenzo Fattori
    More Info: https://github.com/lorenzofattori/M2Q
'''

# used libraries
import logging

# UI stuff
import tkinter as tk

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
def main():
    ''' Initialize the user interface, midi handling and udp communication '''
    # load settings on startup
    settings = config.load_settings()

    # Create UI
    # window = m2q_ui.createUi(settings)
    window = tk.Tk()
    user_interface = UserInterface(window, settings)

    # initialize UDP socket
    udp_socket = m2q_comm.udp_setup()
    user_interface.udp_socket = udp_socket

    # initialize midi
    midiin = m2q_midi.midi_setup(settings, udp_socket, user_interface)
    user_interface.midi_interface = midiin

    # handle shutdown when the windows X is pressed
    # it will be nice to have this in the UserInterface class, but I don't
    # know how to properly handle the midiin port closing and deleting of midiin, any idea?
    window.protocol("WM_DELETE_WINDOW", user_interface.shutdown())

    window.after(5000, m2q_midi.refresh_midi_interfaces, user_interface, window)

    # everything is handled via the input callback, just refresh UI
    window.mainloop()

# Main Function
if __name__ == "__main__":
    main()
