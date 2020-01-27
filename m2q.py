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

# other project files
import m2q_midi
import config
import m2q_comm

# import userinterface

logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s", level=logging.DEBUG
)


def shutdown(midiin):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        midiin.close_port()
        del midiin
        sys.exit()


# Main Function
if __name__ == "__main__":

    # load settings on startup
    settings = config.loadSettings()

    logging.debug("Current Settings:")
    logging.debug(settings)

    # UI Stuff
    window = tk.Tk()
    window.title("M2Q")
    window.configure(background="black")

    # UI - Create main containers
    titleFrame = tk.Frame(window, background="black")
    controlFrame = tk.Frame(window, background="black")
    statusFrame = tk.Frame(window,)

    # UI - layout all of the main containers
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    titleFrame.grid(row=0)
    controlFrame.grid(row=1)
    statusFrame.grid(row=3)

    # UI - Create widgets for the title Frame
    # TODO logo
    titleLabel = tk.Label(
        titleFrame, text="M2Q version 0.1 by Lorenzo Fattori", bg="black", fg="white"
    )

    # UI - Layout widgets for the title frame
    titleLabel.grid(row=0)

    # UI - Create widgets for the control Frame

    settingsLabel = tk.Label(controlFrame, text="Settings", bg="black", fg="white")
    destinationIpLabel = tk.Label(
        controlFrame, text="Destination IP Address:", bg="black", fg="white"
    )
    destinatioIpvalue = tk.Label(
        controlFrame, text=str(settings["destinationIP"]), bg="black", fg="white"
    )

    destinationPortLabel = tk.Label(
        controlFrame, text="Destination Port:", bg="black", fg="white"
    )
    destinationPortValue = tk.Label(
        controlFrame, text=str(settings["destPort"]), bg="black", fg="white"
    )

    cueTriggerLabel = tk.Label(
        controlFrame, text="Cue Trigger:", bg="black", fg="white"
    )
    cueTriggerValue = tk.Label(
        controlFrame, text=settings["jumpMode"], bg="black", fg="white"
    )

    levelTriggerLabel = tk.Label(
        controlFrame, text="Level Trigger:", bg="black", fg="white"
    )
    levelTriggerValue = tk.Label(
        controlFrame, text=settings["levelMode"], bg="black", fg="white"
    )

    cueStackTriggerLabel = tk.Label(
        controlFrame, text="Cue Stack Trigger:", bg="black", fg="white"
    )
    cueStackTriggerValue = tk.Label(
        controlFrame, text=settings["cueStackMode"], bg="black", fg="white"
    )

    tap2TempoTriggerLabel = tk.Label(
        controlFrame, text="Tap2Tempo Trigger:", bg="black", fg="white"
    )
    tap2TempoTriggerValue = tk.Label(
        controlFrame, text=settings["tapToTempoMode"], bg="black", fg="white"
    )
    wingModeLabel = tk.Label(controlFrame, text="Wing Mode:", bg="black", fg="white")
    wingModeValue = tk.Label(
        controlFrame, text=settings["wingMode"], bg="black", fg="white"
    )

    # UI - Layout widgets for the control frame

    settingsLabel.grid(row=0, columnspan=2)
    destinationIpLabel.grid(row=1, column=0)
    destinatioIpvalue.grid(row=1, column=1)

    destinationPortLabel.grid(row=2, column=0)
    destinationPortValue.grid(row=2, column=1)
    cueTriggerLabel.grid(row=3, column=0)
    cueTriggerValue.grid(row=3, column=1)
    levelTriggerLabel.grid(row=4, column=0)
    levelTriggerValue.grid(row=4, column=1)
    cueStackTriggerLabel.grid(row=5, column=0)
    cueStackTriggerValue.grid(row=5, column=1)
    tap2TempoTriggerLabel.grid(row=6, column=0)
    tap2TempoTriggerValue.grid(row=6, column=1)
    wingModeLabel.grid(row=7, column=0)
    wingModeValue.grid(row=7, column=1)

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket)

    # handle shutdown when the windows X is pressed
    window.protocol("WM_DELETE_WINDOW", lambda: shutdown(midiin))

    # everything is handled via the input callback, just refresh UI
    window.mainloop()

