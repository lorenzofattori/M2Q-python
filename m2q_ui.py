import tkinter as tk
from tkinter import messagebox, ttk
import sys

import config


class UserInterface:
    def __init__(self, window, settings):
        self.midiInterface = None
        self.udpSocket = None
        self.window = window

        window.title("M2Q")
        window.configure(background="black")
        window.iconbitmap(r"m2q.ico")

        # Create main containers and lay them out
        self.titleFrame = tk.Frame(window, background="black")
        self.controlFrame = tk.Frame(window, background="black")
        self.statusFrame = tk.Frame(window, background="black")

        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.titleFrame.grid(row=0)
        self.controlFrame.grid(row=1)
        self.statusFrame.grid(row=3)

        # Populate Frame title and lay it out
        self.logoCanvas = tk.Canvas(
            self.titleFrame, width=350, height=240, bg="black", highlightthickness=0
        )

        self.logoImg = tk.PhotoImage(file="m2q-logo-v2.png")
        self.logoCanvas.create_image(175, 80, image=self.logoImg)
        self.fakeLabel = tk.Label(image=self.logoImg)
        self.fakeLabel.image = self.logoImg  # keep a reference if not desappears

        self.img = tk.PhotoImage(file="m2q-logo-v2-text.png")
        self.logoCanvas.create_image(175, 188, image=self.img)
        self.fakeLabel = tk.Label(image=self.img)
        self.fakeLabel.image = self.img  # keep a reference if not desappears

        self.titleLabel = tk.Label(
            self.titleFrame,
            text="Version 1.0   by Lorenzo Fattori",
            bg="black",
            fg="white",
            font="Helvetica 16 bold",
        )

        self.lineLabel = tk.Label(
            self.titleFrame,
            text="_________________________",
            bg="black",
            fg="white",
            font="Helvetica 18 bold",
        )

        self.logoCanvas.grid(row=0)
        self.titleLabel.grid(row=1)
        self.lineLabel.grid(row=2)

        # Control Frame
        self.settingsLabel = tk.Label(
            self.controlFrame,
            text="Settings",
            bg="black",
            fg="white",
            font="Helvetica 16 bold",
        )
        self.settingsLabel.config(anchor="w")

        self.interfacesLabel = tk.Label(
            self.controlFrame,
            text="MIDI Interface:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        style = ttk.Style()
        style.configure(
            "TLabel", foreground="white", background="black",
        )
        self.interfacesList = []
        self.interfacesValue = ttk.Combobox(
            self.controlFrame, values=self.interfacesList, style="TLabel"
        )

        self.interfacesSetButton = tk.Button(
            self.controlFrame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.setInterface(self.interfacesValue, settings),
        )

        self.destinationIpLabel = tk.Label(
            self.controlFrame,
            text="Destination IP Address:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        self.destinationIpTkVar = tk.StringVar()
        self.destinationIpTkVar.set(settings["destinationIP"])
        self.destinationIpValue = tk.Entry(
            self.controlFrame,
            bg="black",
            fg="white",
            insertbackground="white",
            textvariable=self.destinationIpTkVar,
        )

        self.destinationIpSetButton = tk.Button(
            self.controlFrame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.setDestinationIp(
                self.destinationIpValue.get(), "destinationIP", settings
            ),
        )

        self.destinationPortLabel = tk.Label(
            self.controlFrame,
            text="Destination Port:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        self.destinationPortTkVar = tk.IntVar()
        self.destinationPortTkVar.set(settings["destPort"])
        self.destinationPortValue = tk.Entry(
            self.controlFrame,
            bg="black",
            fg="white",
            insertbackground="white",
            textvariable=self.destinationPortTkVar,
        )

        self.destinationPortSetButton = tk.Button(
            self.controlFrame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.setDestinationIp(
                int(self.destinationPortValue.get()), "destPort", settings
            ),
        )

        # Checkbox for Settings
        self.cueTriggerTkVar = tk.BooleanVar()
        self.cueTriggerTkVar.set(bool(settings["jumpMode"]))
        self.cueTriggerValue = tk.Checkbutton(
            self.controlFrame,
            text="Cue Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.cueTriggerTkVar,
            command=lambda: self.toggleCheckboxValue(
                self.cueTriggerTkVar.get(), "jumpMode", settings
            ),
        )

        self.levelTriggerTkVar = tk.BooleanVar()
        self.levelTriggerTkVar.set(bool(settings["levelMode"]))
        self.levelTriggerValue = tk.Checkbutton(
            self.controlFrame,
            text="Level Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.levelTriggerTkVar,
            command=lambda: self.toggleCheckboxValue(
                self.levelTriggerTkVar.get(), "levelMode", settings
            ),
        )

        self.cueStackTriggerTkVar = tk.BooleanVar()
        self.cueStackTriggerTkVar.set(bool(settings["cueStackMode"]))
        self.cueStackTriggerValue = tk.Checkbutton(
            self.controlFrame,
            text="CueStack Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.cueStackTriggerTkVar,
            command=lambda: self.toggleCheckboxValue(
                self.cueStackTriggerTkVar.get(), "cueStackMode", settings
            ),
        )

        self.tap2TempoTriggerTkVar = tk.BooleanVar()
        self.tap2TempoTriggerTkVar.set(bool(settings["tapToTempoMode"]))
        self.tap2TempoTriggerValue = tk.Checkbutton(
            self.controlFrame,
            text="Tap2Tempo Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.tap2TempoTriggerTkVar,
            command=lambda: self.toggleCheckboxValue(
                self.tap2TempoTriggerTkVar.get(), "tapToTempoMode", settings
            ),
        )

        self.wingModeTkVar = tk.BooleanVar()
        self.wingModeTkVar.set(bool(settings["wingMode"]))
        self.wingModeValue = tk.Checkbutton(
            self.controlFrame,
            text="Wing Mode",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.wingModeTkVar,
            command=lambda: self.toggleCheckboxValue(
                self.wingModeTkVar.get(), "wingMode", settings
            ),
        )

        # Save and Load Settings Buttons
        self.saveSettingsButton = tk.Button(
            self.controlFrame,
            bg="black",
            fg="white",
            text="Save Settings",
            width=15,
            font="Helvetica 10 bold",
            command=lambda: self.saveSettings(settings),
        )

        # self.loadSettingsButton = tk.Button(
        #     self.controlFrame,
        #     bg="black",
        #     fg="white",
        #     text="Load Settings",
        #     width=15,
        #     #command=lambda: self.loadSettings(window),
        # )

        self.settingsLabel.grid(row=0, columnspan=3, pady=5)
        self.controlFrame.grid_rowconfigure(1, minsize=10)

        self.interfacesLabel.grid(sticky="W", row=1, column=0)
        self.interfacesValue.grid(row=1, column=1)
        self.interfacesSetButton.grid(row=1, column=2, padx=2)

        self.destinationIpLabel.grid(sticky="W", row=2, column=0)
        self.destinationIpValue.grid(row=2, column=1, padx=5)
        self.destinationIpSetButton.grid(row=2, column=2, padx=2)

        self.destinationPortLabel.grid(sticky="W", row=3, column=0)
        self.destinationPortValue.grid(row=3, column=1, padx=5)
        self.destinationPortSetButton.grid(row=3, column=2, padx=2)

        self.cueTriggerValue.grid(sticky="W", row=4, column=0, columnspan=2)
        self.levelTriggerValue.grid(sticky="W", row=5, column=0, columnspan=2)
        self.cueStackTriggerValue.grid(sticky="W", row=6, column=0, columnspan=2)
        self.tap2TempoTriggerValue.grid(sticky="W", row=7, column=0, columnspan=2)
        self.wingModeValue.grid(sticky="W", row=9, column=0, columnspan=2)

        self.saveSettingsButton.grid(row=6, column=1, columnspan=2, padx=5)
        # self.loadSettingsButton.grid(row=8, column=1)

        # Populate Status frame and lay it out
        self.lineLabel2 = tk.Label(
            self.statusFrame,
            text="_________________________",
            bg="black",
            fg="white",
            font="Helvetica 18 bold",
        )

        self.lineLabel2.grid(row=0)

        self.midiInLabel = tk.Label(
            self.statusFrame,
            text="MIDI IN",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )
        self.midiInLabel.grid(sticky="W", row=1, column=0)

        self.chamsysOutLabel = tk.Label(
            self.statusFrame,
            text="CHAMSYS OUT",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )
        self.chamsysOutLabel.grid(sticky="E", row=1, column=0)

        self.errorLabel = tk.Label(
            self.statusFrame,
            text="ERROR",
            bg="black",
            fg="black",
            font="Helvetica 12 bold",
        )
        self.errorLabel.grid(row=2, column=0)

    def setInterface(self, entryValue, settings):
        """
        Handles the set button of the new interface
        I don't know exactly how to do it, so for now it saves settings and close the program
        help will be apprecated here
        """

        from m2q_midi import changeMidiPort
        changeMidiPort(self, entryValue.current(), settings)

        settings["interface"] = entryValue.get()
        config.saveSettings(settings)

    def setDestinationIp(self, entryValue, whichSetting, settings):
        """
        This function handles changes of the entry values for interface, IP address and port
        It's called by when pressing one of the Set vuttons, and changes the current settings with the new value
        """
        # TODO, make a validation check before setting it?
        # print(f"entryValue is {entryValue}")
        settings[whichSetting] = entryValue

    def toggleCheckboxValue(self, toggleValue, whichSetting, settings):
        """
        This function handles the clicking of the CheckBox for settings
        It's called by the checkbox itselfs, it checks if the checkbox is selected or not and changes the current settings with the new value
        """
        # print(f"toggleValue is {toggleValue}")
        if toggleValue == True:
            settings[whichSetting] = 1
        else:
            settings[whichSetting] = 0

    def saveSettings(self, settings):
        """
        Called when ckicking on Save Settings
        """
        if messagebox.askokcancel("Save Settings", "Do you want to save settings?"):
            config.saveSettings(settings)

    def shutdown(self, midiin):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            if self.midi_interface:
                self.midi_interface.close_port()
                del self.midi_interface
            sys.exit()

    def flash(self, whichValue):
        """
        Flash the IN/OUT labels when a midi message is received or a chamsys out message is sent out+
        whichValue can be "MIDI", "chamsys" or "ERROR"
        """

        if whichValue == "MIDI":
            self.midiInLabel.config(fg="#C01914")
            self.midiInLabel.after(200, lambda: self.midiInLabel.config(fg="white"))

        if whichValue == "chamsys":
            self.chamsysOutLabel.config(fg="#C01914")
            self.chamsysOutLabel.after(
                200, lambda: self.chamsysOutLabel.config(fg="white")
            )

        if whichValue == "ERROR":
            self.errorLabel.config(fg="#C01914")
            self.errorLabel.after(1000, lambda: self.errorLabel.config(fg="black"))
