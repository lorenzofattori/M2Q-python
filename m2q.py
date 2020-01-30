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


# UI toggle button functions
def toggleCheckboxValue(toggleValue, whichSetting):
    """
    This function handles the clicking of the CheckBox for settings
    It's called by the checkbox itselfs, it checks if the checkbox is selected or not and changes the current settings with the new value
    """
    print(f"toggleValue is {toggleValue}")
    if toggleValue == True:
        settings[whichSetting] = 1
    else:
        settings[whichSetting] = 0


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

    # Checkbox for Settings
    cueTriggerTkVar = tk.BooleanVar()
    cueTriggerTkVar.set(bool(settings["jumpMode"]))
    cueTriggerValue = tk.Checkbutton(
        controlFrame,
        text="Cue Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        variable=cueTriggerTkVar,
        command=lambda: toggleCheckboxValue(cueTriggerTkVar.get(), "jumpMode"),
    )

    levelTriggerTkVar = tk.BooleanVar()
    levelTriggerTkVar.set(bool(settings["levelMode"]))
    levelTriggerValue = tk.Checkbutton(
        controlFrame,
        text="Level Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        variable=levelTriggerTkVar,
        command=lambda: toggleCheckboxValue(levelTriggerTkVar.get(), "levelMode"),
    )

    cueStackTriggerTkVar = tk.BooleanVar()
    cueStackTriggerTkVar.set(bool(settings["cueStackMode"]))
    cueStackTriggerValue = tk.Checkbutton(
        controlFrame,
        text="CueStack Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        variable=cueStackTriggerTkVar,
        command=lambda: toggleCheckboxValue(cueStackTriggerTkVar.get(), "cueStackMode"),
    )

    tap2TempoTriggerTkVar = tk.BooleanVar()
    tap2TempoTriggerTkVar.set(bool(settings["tapToTempoMode"]))
    tap2TempoTriggerValue = tk.Checkbutton(
        controlFrame,
        text="Tap2Tempo Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        variable=tap2TempoTriggerTkVar,
        command=lambda: toggleCheckboxValue(
            tap2TempoTriggerTkVar.get(), "tapToTempoMode"
        ),
    )

    wingModeTkVar = tk.BooleanVar()
    wingModeTkVar.set(bool(settings["wingMode"]))
    wingModeValue = tk.Checkbutton(
        controlFrame,
        text="Wing Mode",
        bg="black",
        fg="white",
        selectcolor="black",
        variable=wingModeTkVar,
        command=lambda: toggleCheckboxValue(wingModeTkVar.get(), "wingMode"),
    )

    # UI - Layout widgets for the control frame

    settingsLabel.grid(row=0, columnspan=2)
    destinationIpLabel.grid(row=1, column=0)
    destinatioIpvalue.grid(row=1, column=1)

    destinationPortLabel.grid(row=2, column=0)
    destinationPortValue.grid(row=2, column=1)
    cueTriggerValue.grid(row=3, column=1)
    levelTriggerValue.grid(row=4, column=1)
    cueStackTriggerValue.grid(row=5, column=1)
    tap2TempoTriggerValue.grid(row=6, column=1)
    wingModeValue.grid(row=7, column=1)

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket)

    # handle shutdown when the windows X is pressed
    window.protocol("WM_DELETE_WINDOW", lambda: shutdown(midiin))

    # everything is handled via the input callback, just refresh UI
    window.mainloop()

