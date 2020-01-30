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


def setDestinationIp(entryValue, whichSetting):
    """
    This function handles changes of the entry values for IP address and port
    It's called by when pressing one of the Set vuttons, and changes the current settings with the new value
    """
    # TODO, make a validation check before setting it?
    settings[whichSetting] = entryValue


def saveSettings():
    """
    Called when ckicking on Save Settings
    """
    if messagebox.askokcancel("Save Settings", "Do you want to save settings?"):
        config.saveSettings(settings)


def createUi():
    """
    Generates the main UI window
    """
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

    destinationIpTkVar = tk.StringVar()
    destinationIpTkVar.set(settings["destinationIP"])
    destinationIpValue = tk.Entry(
        controlFrame,
        bg="black",
        fg="white",
        insertbackground="white",
        textvariable=destinationIpTkVar,
    )

    destinationIpSetButton = tk.Button(
        controlFrame,
        bg="black",
        fg="white",
        text="Set",
        width=5,
        command=lambda: setDestinationIp(destinationIpValue.get(), "destinationIP"),
    )

    destinationPortLabel = tk.Label(
        controlFrame, text="Destination Port:", bg="black", fg="white"
    )

    destinationPortTkVar = tk.IntVar()
    destinationPortTkVar.set(settings["destPort"])
    destinationPortValue = tk.Entry(
        controlFrame,
        bg="black",
        fg="white",
        insertbackground="white",
        textvariable=destinationPortTkVar,
    )

    destinationPortSetButton = tk.Button(
        controlFrame,
        bg="black",
        fg="white",
        text="Set",
        width=5,
        command=lambda: setDestinationIp(int(destinationPortValue.get()), "destPort"),
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

    # Save Settings Button
    saveSettingsButton = tk.Button(
        controlFrame,
        bg="black",
        fg="white",
        text="Save Settings",
        width=15,
        command=saveSettings,
    )

    # Load Settings Button
    loadSettingsButton = tk.Button(
        controlFrame,
        bg="black",
        fg="white",
        text="Load Settings",
        width=15,
        command=lambda: loadSettings(window),
    )

    # UI - Layout widgets for the control frame
    settingsLabel.grid(row=0, columnspan=2)

    destinationIpLabel.grid(row=1, column=0)
    destinationIpValue.grid(row=1, column=1)
    destinationIpSetButton.grid(row=1, column=3)

    destinationPortLabel.grid(row=2, column=0)
    destinationPortValue.grid(row=2, column=1)
    destinationPortSetButton.grid(row=2, column=3)

    cueTriggerValue.grid(sticky="W", row=3, column=0, columnspan=2, padx=50)
    levelTriggerValue.grid(sticky="W", row=4, column=0, columnspan=2, padx=50)
    cueStackTriggerValue.grid(sticky="W", row=5, column=0, columnspan=2, padx=50)
    tap2TempoTriggerValue.grid(sticky="W", row=6, column=0, columnspan=2, padx=50)
    wingModeValue.grid(sticky="W", row=7, column=0, columnspan=2, padx=50)

    saveSettingsButton.grid(row=8, column=0)
    # loadSettingsButton.grid(row=8, column=1)

    return window


# Main Function
if __name__ == "__main__":

    # load settings on startup
    settings = config.loadSettings()

    # Create UI
    window = createUi()

    # # UI Stuff
    # window = tk.Tk()
    # window.title("M2Q")
    # window.configure(background="black")

    # # UI - Create main containers
    # titleFrame = tk.Frame(window, background="black")
    # controlFrame = tk.Frame(window, background="black")
    # statusFrame = tk.Frame(window,)

    # # UI - layout all of the main containers
    # window.grid_rowconfigure(1, weight=1)
    # window.grid_columnconfigure(0, weight=1)

    # titleFrame.grid(row=0)
    # controlFrame.grid(row=1)
    # statusFrame.grid(row=3)

    # # UI - Create widgets for the title Frame
    # # TODO logo
    # titleLabel = tk.Label(
    #     titleFrame, text="M2Q version 0.1 by Lorenzo Fattori", bg="black", fg="white"
    # )

    # # UI - Layout widgets for the title frame
    # titleLabel.grid(row=0)

    # # UI - Create widgets for the control Frame
    # settingsLabel = tk.Label(controlFrame, text="Settings", bg="black", fg="white")
    # destinationIpLabel = tk.Label(
    #     controlFrame, text="Destination IP Address:", bg="black", fg="white"
    # )

    # destinationIpTkVar = tk.StringVar()
    # destinationIpTkVar.set(settings["destinationIP"])
    # destinationIpValue = tk.Entry(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     insertbackground="white",
    #     textvariable=destinationIpTkVar,
    # )

    # destinationIpSetButton = tk.Button(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     text="Set",
    #     width=5,
    #     command=lambda: setDestinationIp(destinationIpValue.get(), "destinationIP"),
    # )

    # destinationPortLabel = tk.Label(
    #     controlFrame, text="Destination Port:", bg="black", fg="white"
    # )

    # destinationPortTkVar = tk.IntVar()
    # destinationPortTkVar.set(settings["destPort"])
    # destinationPortValue = tk.Entry(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     insertbackground="white",
    #     textvariable=destinationPortTkVar,
    # )

    # destinationPortSetButton = tk.Button(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     text="Set",
    #     width=5,
    #     command=lambda: setDestinationIp(int(destinationPortValue.get()), "destPort"),
    # )

    # # Checkbox for Settings
    # cueTriggerTkVar = tk.BooleanVar()
    # cueTriggerTkVar.set(bool(settings["jumpMode"]))
    # cueTriggerValue = tk.Checkbutton(
    #     controlFrame,
    #     text="Cue Trigger",
    #     bg="black",
    #     fg="white",
    #     selectcolor="black",
    #     variable=cueTriggerTkVar,
    #     command=lambda: toggleCheckboxValue(cueTriggerTkVar.get(), "jumpMode"),
    # )

    # levelTriggerTkVar = tk.BooleanVar()
    # levelTriggerTkVar.set(bool(settings["levelMode"]))
    # levelTriggerValue = tk.Checkbutton(
    #     controlFrame,
    #     text="Level Trigger",
    #     bg="black",
    #     fg="white",
    #     selectcolor="black",
    #     variable=levelTriggerTkVar,
    #     command=lambda: toggleCheckboxValue(levelTriggerTkVar.get(), "levelMode"),
    # )

    # cueStackTriggerTkVar = tk.BooleanVar()
    # cueStackTriggerTkVar.set(bool(settings["cueStackMode"]))
    # cueStackTriggerValue = tk.Checkbutton(
    #     controlFrame,
    #     text="CueStack Trigger",
    #     bg="black",
    #     fg="white",
    #     selectcolor="black",
    #     variable=cueStackTriggerTkVar,
    #     command=lambda: toggleCheckboxValue(cueStackTriggerTkVar.get(), "cueStackMode"),
    # )

    # tap2TempoTriggerTkVar = tk.BooleanVar()
    # tap2TempoTriggerTkVar.set(bool(settings["tapToTempoMode"]))
    # tap2TempoTriggerValue = tk.Checkbutton(
    #     controlFrame,
    #     text="Tap2Tempo Trigger",
    #     bg="black",
    #     fg="white",
    #     selectcolor="black",
    #     variable=tap2TempoTriggerTkVar,
    #     command=lambda: toggleCheckboxValue(
    #         tap2TempoTriggerTkVar.get(), "tapToTempoMode"
    #     ),
    # )

    # wingModeTkVar = tk.BooleanVar()
    # wingModeTkVar.set(bool(settings["wingMode"]))
    # wingModeValue = tk.Checkbutton(
    #     controlFrame,
    #     text="Wing Mode",
    #     bg="black",
    #     fg="white",
    #     selectcolor="black",
    #     variable=wingModeTkVar,
    #     command=lambda: toggleCheckboxValue(wingModeTkVar.get(), "wingMode"),
    # )

    # # Save Settings Button
    # saveSettingsButton = tk.Button(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     text="Save Settings",
    #     width=15,
    #     command=saveSettings,
    # )

    # # Load Settings Button
    # loadSettingsButton = tk.Button(
    #     controlFrame,
    #     bg="black",
    #     fg="white",
    #     text="Load Settings",
    #     width=15,
    #     command=loadSettings,
    # )

    # # UI - Layout widgets for the control frame
    # settingsLabel.grid(row=0, columnspan=2)

    # destinationIpLabel.grid(row=1, column=0)
    # destinationIpValue.grid(row=1, column=1)
    # destinationIpSetButton.grid(row=1, column=3)

    # destinationPortLabel.grid(row=2, column=0)
    # destinationPortValue.grid(row=2, column=1)
    # destinationPortSetButton.grid(row=2, column=3)

    # cueTriggerValue.grid(sticky="W", row=3, column=0, columnspan=2, padx=50)
    # levelTriggerValue.grid(sticky="W", row=4, column=0, columnspan=2, padx=50)
    # cueStackTriggerValue.grid(sticky="W", row=5, column=0, columnspan=2, padx=50)
    # tap2TempoTriggerValue.grid(sticky="W", row=6, column=0, columnspan=2, padx=50)
    # wingModeValue.grid(sticky="W", row=7, column=0, columnspan=2, padx=50)

    # saveSettingsButton.grid(row=8, column=0)
    # loadSettingsButton.grid(row=8, column=1)

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket)

    # handle shutdown when the windows X is pressed
    window.protocol("WM_DELETE_WINDOW", lambda: shutdown(midiin))

    # everything is handled via the input callback, just refresh UI
    window.mainloop()

