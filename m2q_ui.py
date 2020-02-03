import tkinter as tk
from tkinter import messagebox
import sys

import config


def shutdown(midiin, window):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        midiin.close_port()
        del midiin
        sys.exit()


# UI toggle button functions
def toggleCheckboxValue(toggleValue, whichSetting, settings):
    """
    This function handles the clicking of the CheckBox for settings
    It's called by the checkbox itselfs, it checks if the checkbox is selected or not and changes the current settings with the new value
    """
    #print(f"toggleValue is {toggleValue}")
    if toggleValue == True:
        settings[whichSetting] = 1
    else:
        settings[whichSetting] = 0


def setDestinationIp(entryValue, whichSetting, settings):
    """
    This function handles changes of the entry values for IP address and port
    It's called by when pressing one of the Set vuttons, and changes the current settings with the new value
    """
    # TODO, make a validation check before setting it?
    settings[whichSetting] = entryValue


def saveSettings(settings):
    """
    Called when ckicking on Save Settings
    """
    if messagebox.askokcancel("Save Settings", "Do you want to save settings?"):
        config.saveSettings(settings)


def createUi(settings):
    """
    Generates the main UI window
    """
    # UI Stuff
    window = tk.Tk()
    window.title("M2Q")
    window.configure(background="black")
    window.iconbitmap(r"m2q.ico")

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

    # M2Q Logo
    logoCanvas = tk.Canvas(
        titleFrame, width=350, height=240, bg="black", highlightthickness=0
    )

    logoImg = tk.PhotoImage(file="m2q-logo-v2.png")
    logoCanvas.create_image(175, 80, image=logoImg)
    label = tk.Label(image=logoImg)
    label.image = logoImg  # keep a reference if not desappears

    img = tk.PhotoImage(file="m2q-logo-v2-text.png")
    logoCanvas.create_image(175, 188, image=img)
    label = tk.Label(image=img)
    label.image = img  # keep a reference if not desappears

    titleLabel = tk.Label(
        titleFrame,
        text="Version 1.0   by Lorenzo Fattori",
        bg="black",
        fg="white",
        font="Helvetica 16 bold",
    )

    lineLabel = tk.Label(
        titleFrame,
        text="_________________________",
        bg="black",
        fg="white",
        font="Helvetica 18 bold",
    )

    # UI - Layout widgets for the title frame
    logoCanvas.grid(row=0)
    titleLabel.grid(row=1)
    lineLabel.grid(row=2)

    # UI - Create widgets for the control Frame
    settingsLabel = tk.Label(
        controlFrame, text="Settings", bg="black", fg="white", font="Helvetica 16 bold",
    )
    settingsLabel.config(anchor="w")

    destinationIpLabel = tk.Label(
        controlFrame,
        text="Destination IP Address:",
        bg="black",
        fg="white",
        font="Helvetica 10 bold",
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
        command=lambda: setDestinationIp(
            destinationIpValue.get(), "destinationIP", settings
        ),
    )

    destinationPortLabel = tk.Label(
        controlFrame,
        text="Destination Port:",
        bg="black",
        fg="white",
        font="Helvetica 10 bold",
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
        command=lambda: setDestinationIp(
            int(destinationPortValue.get()), "destPort", settings
        ),
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
        font="Helvetica 10 bold",
        variable=cueTriggerTkVar,
        command=lambda: toggleCheckboxValue(
            cueTriggerTkVar.get(), "jumpMode", settings
        ),
    )

    levelTriggerTkVar = tk.BooleanVar()
    levelTriggerTkVar.set(bool(settings["levelMode"]))
    levelTriggerValue = tk.Checkbutton(
        controlFrame,
        text="Level Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        font="Helvetica 10 bold",
        variable=levelTriggerTkVar,
        command=lambda: toggleCheckboxValue(
            levelTriggerTkVar.get(), "levelMode", settings
        ),
    )

    cueStackTriggerTkVar = tk.BooleanVar()
    cueStackTriggerTkVar.set(bool(settings["cueStackMode"]))
    cueStackTriggerValue = tk.Checkbutton(
        controlFrame,
        text="CueStack Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        font="Helvetica 10 bold",
        variable=cueStackTriggerTkVar,
        command=lambda: toggleCheckboxValue(
            cueStackTriggerTkVar.get(), "cueStackMode", settings
        ),
    )

    tap2TempoTriggerTkVar = tk.BooleanVar()
    tap2TempoTriggerTkVar.set(bool(settings["tapToTempoMode"]))
    tap2TempoTriggerValue = tk.Checkbutton(
        controlFrame,
        text="Tap2Tempo Trigger",
        bg="black",
        fg="white",
        selectcolor="black",
        font="Helvetica 10 bold",
        variable=tap2TempoTriggerTkVar,
        command=lambda: toggleCheckboxValue(
            tap2TempoTriggerTkVar.get(), "tapToTempoMode", settings
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
        font="Helvetica 10 bold",
        variable=wingModeTkVar,
        command=lambda: toggleCheckboxValue(wingModeTkVar.get(), "wingMode", settings),
    )

    # Save Settings Button
    saveSettingsButton = tk.Button(
        controlFrame,
        bg="black",
        fg="white",
        text="Save Settings",
        width=15,
        font="Helvetica 10 bold",
        command=lambda: saveSettings(settings),
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
    settingsLabel.grid(row=0, columnspan=3, pady=5)
    controlFrame.grid_rowconfigure(1, minsize=10)

    destinationIpLabel.grid(sticky="W", row=2, column=0)
    destinationIpValue.grid(row=2, column=1, padx=5)
    destinationIpSetButton.grid(row=2, column=2, padx=2)

    destinationPortLabel.grid(sticky="W", row=3, column=0)
    destinationPortValue.grid(row=3, column=1, padx=5)
    destinationPortSetButton.grid(row=3, column=2, padx=2)

    cueTriggerValue.grid(sticky="W", row=4, column=0, columnspan=2)
    levelTriggerValue.grid(sticky="W", row=5, column=0, columnspan=2)
    cueStackTriggerValue.grid(sticky="W", row=6, column=0, columnspan=2)
    tap2TempoTriggerValue.grid(sticky="W", row=7, column=0, columnspan=2)
    wingModeValue.grid(sticky="W", row=9, column=0, columnspan=2)

    saveSettingsButton.grid(row=10, column=0, pady=15)
    # loadSettingsButton.grid(row=8, column=1)

    return window

