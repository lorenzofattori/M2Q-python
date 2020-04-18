import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

import config
from m2q_midi import change_midi_port


class UserInterface:
    def __init__(self, window, settings):
        self.midi_interface = None
        self.udp_socket = None
        self.window = window

        window.title("M2Q")
        window.configure(background="black")

        # PyInstaller has a different path for the icon file so we need to find it
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS # pylint: disable=no-member
        elif __file__:
            application_path = os.path.dirname(__file__)

        window.iconbitmap(os.path.join(application_path, "m2q.ico"))

        # Create main containers and lay them out
        self.title_frame = tk.Frame(window, background="black")
        self.control_frame = tk.Frame(window, background="black")
        self.status_frame = tk.Frame(window, background="black")

        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.title_frame.grid(row=0)
        self.control_frame.grid(row=1)
        self.status_frame.grid(row=3)

        # Populate Frame title and lay it out
        self.logo_canvas = tk.Canvas(
            self.title_frame, width=350, height=240, bg="black", highlightthickness=0
        )

        self.logo_img = tk.PhotoImage(file=os.path.join(application_path, "m2q-logo-v2.png"))
        self.logo_canvas.create_image(175, 80, image=self.logo_img)
        self.fake_label = tk.Label(image=self.logo_img)
        self.fake_label.image = self.logo_img  # keep a reference if not desappears

        self.img = tk.PhotoImage(file=os.path.join(application_path, "m2q-logo-v2-text.png"))
        self.logo_canvas.create_image(175, 188, image=self.img)
        self.fake_label = tk.Label(image=self.img)
        self.fake_label.image = self.img  # keep a reference if not desappears

        self.title_label = tk.Label(
            self.title_frame,
            text="Version 1.0   by Lorenzo Fattori",
            bg="black",
            fg="white",
            font="Helvetica 16 bold",
        )

        self.line_label = tk.Label(
            self.title_frame,
            text="_________________________",
            bg="black",
            fg="white",
            font="Helvetica 18 bold",
        )

        self.logo_canvas.grid(row=0)
        self.title_label.grid(row=1)
        self.line_label.grid(row=2)

        # Control Frame
        self.settings_label = tk.Label(
            self.control_frame,
            text="Settings",
            bg="black",
            fg="white",
            font="Helvetica 16 bold",
        )
        self.settings_label.config(anchor="w")

        self.interfaces_label = tk.Label(
            self.control_frame,
            text="MIDI Interface:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        style = ttk.Style()
        style.configure(
            "TLabel", foreground="white", background="black",
        )
        self.interfaces_list = []
        self.interfaces_value = ttk.Combobox(
            self.control_frame, values=self.interfaces_list, style="TLabel"
        )

        self.interfaces_set_button = tk.Button(
            self.control_frame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.set_interface(self.interfaces_value, settings),
        )

        self.destination_ip_label = tk.Label(
            self.control_frame,
            text="Destination IP Address:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        self.destination_ip_tk_var = tk.StringVar()
        self.destination_ip_tk_var.set(settings["destinationIP"])
        self.destination_ip_value = tk.Entry(
            self.control_frame,
            bg="black",
            fg="white",
            insertbackground="white",
            textvariable=self.destination_ip_tk_var,
        )

        self.destination_ip_set_button = tk.Button(
            self.control_frame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.set_destination_ip(
                self.destination_ip_value.get(), "destinationIP", settings
            ),
        )

        self.destination_port_label = tk.Label(
            self.control_frame,
            text="Destination Port:",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )

        self.destination_port_tk_var = tk.IntVar()
        self.destination_port_tk_var.set(settings["destPort"])
        self.destination_port_value = tk.Entry(
            self.control_frame,
            bg="black",
            fg="white",
            insertbackground="white",
            textvariable=self.destination_port_tk_var,
        )

        self.destination_port_set_button = tk.Button(
            self.control_frame,
            bg="black",
            fg="white",
            text="Set",
            width=5,
            command=lambda: self.set_destination_ip(
                int(self.destination_port_value.get()), "destPort", settings
            ),
        )

        # Checkbox for Settings
        self.cue_trigger_tk_var = tk.BooleanVar()
        self.cue_trigger_tk_var.set(bool(settings["jumpMode"]))
        self.cue_trigger_value = tk.Checkbutton(
            self.control_frame,
            text="Cue Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.cue_trigger_tk_var,
            command=lambda: self.toggle_checkbox_value(
                self.cue_trigger_tk_var.get(), "jumpMode", settings
            ),
        )

        self.level_trigger_tk_var = tk.BooleanVar()
        self.level_trigger_tk_var.set(bool(settings["levelMode"]))
        self.level_trigger_value = tk.Checkbutton(
            self.control_frame,
            text="Level Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.level_trigger_tk_var,
            command=lambda: self.toggle_checkbox_value(
                self.level_trigger_tk_var.get(), "levelMode", settings
            ),
        )

        self.cue_stack_trigger_tk_var = tk.BooleanVar()
        self.cue_stack_trigger_tk_var.set(bool(settings["cueStackMode"]))
        self.cue_stack_trigger_value = tk.Checkbutton(
            self.control_frame,
            text="CueStack Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.cue_stack_trigger_tk_var,
            command=lambda: self.toggle_checkbox_value(
                self.cue_stack_trigger_tk_var.get(), "cueStackMode", settings
            ),
        )

        self.tap_2_tempo_trigger_tk_var = tk.BooleanVar()
        self.tap_2_tempo_trigger_tk_var.set(bool(settings["tapToTempoMode"]))
        self.tap_2_tempo_trigger_value = tk.Checkbutton(
            self.control_frame,
            text="Tap2Tempo Trigger",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.tap_2_tempo_trigger_tk_var,
            command=lambda: self.toggle_checkbox_value(
                self.tap_2_tempo_trigger_tk_var.get(), "tapToTempoMode", settings
            ),
        )

        self.wing_mode_tk_var = tk.BooleanVar()
        self.wing_mode_tk_var.set(bool(settings["wingMode"]))
        self.wing_mode_value = tk.Checkbutton(
            self.control_frame,
            text="Wing Mode",
            bg="black",
            fg="white",
            selectcolor="black",
            font="Helvetica 10 bold",
            variable=self.wing_mode_tk_var,
            command=lambda: self.toggle_checkbox_value(
                self.wing_mode_tk_var.get(), "wingMode", settings
            ),
        )

        # Save and Load Settings Buttons
        self.save_settings_button = tk.Button(
            self.control_frame,
            bg="black",
            fg="white",
            text="Save Settings",
            width=15,
            font="Helvetica 10 bold",
            command=lambda: self.save_settings(settings),
        )

        # self.loadSettingsButton = tk.Button(
        #     self.control_frame,
        #     bg="black",
        #     fg="white",
        #     text="Load Settings",
        #     width=15,
        #     #command=lambda: self.loadSettings(window),
        # )

        self.settings_label.grid(row=0, columnspan=3, pady=5)
        self.control_frame.grid_rowconfigure(1, minsize=10)

        self.interfaces_label.grid(sticky="W", row=1, column=0)
        self.interfaces_value.grid(row=1, column=1)
        self.interfaces_set_button.grid(row=1, column=2, padx=2)

        self.destination_ip_label.grid(sticky="W", row=2, column=0)
        self.destination_ip_value.grid(row=2, column=1, padx=5)
        self.destination_ip_set_button.grid(row=2, column=2, padx=2)

        self.destination_port_label.grid(sticky="W", row=3, column=0)
        self.destination_port_value.grid(row=3, column=1, padx=5)
        self.destination_port_set_button.grid(row=3, column=2, padx=2)

        self.cue_trigger_value.grid(sticky="W", row=4, column=0, columnspan=2)
        self.level_trigger_value.grid(sticky="W", row=5, column=0, columnspan=2)
        self.cue_stack_trigger_value.grid(sticky="W", row=6, column=0, columnspan=2)
        self.tap_2_tempo_trigger_value.grid(sticky="W", row=7, column=0, columnspan=2)
        self.wing_mode_value.grid(sticky="W", row=9, column=0, columnspan=2)

        self.save_settings_button.grid(row=6, column=1, columnspan=2, padx=5)
        # self.loadSettingsButton.grid(row=8, column=1)

        # Populate Status frame and lay it out
        self.line_label_2 = tk.Label(
            self.status_frame,
            text="_________________________",
            bg="black",
            fg="white",
            font="Helvetica 18 bold",
        )

        self.line_label_2.grid(row=0)

        self.midi_in_label = tk.Label(
            self.status_frame,
            text="MIDI IN",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )
        self.midi_in_label.grid(sticky="W", row=1, column=0)

        self.chamsys_out_label = tk.Label(
            self.status_frame,
            text="CHAMSYS OUT",
            bg="black",
            fg="white",
            font="Helvetica 10 bold",
        )
        self.chamsys_out_label.grid(sticky="E", row=1, column=0)

        self.error_label = tk.Label(
            self.status_frame,
            text="ERROR",
            bg="black",
            fg="black",
            font="Helvetica 12 bold",
        )
        self.error_label.grid(row=2, column=0)

    def set_interface(self, entry_value, settings):
        """
        Handles the set button of the new interface
        I don't know exactly how to do it, so for now it saves settings and close the program
        help will be apprecated here
        """

        change_midi_port(self, entry_value.current(), settings)

        settings["interface"] = entry_value.get()
        config.save_settings(settings)

    def set_destination_ip(self, entry_value, which_setting, settings):
        """
        This function handles changes of the entry values for interface, IP address and port
        It's called by when pressing one of the Set vuttons, and changes the
        current settings with the new value
        """
        # TODO, make a validation check before setting it?
        # print(f"entryValue is {entryValue}")
        settings[which_setting] = entry_value

    def toggle_checkbox_value(self, toggle_value, which_setting, settings):
        """
        This function handles the clicking of the CheckBox for settings
        It's called by the checkbox itselfs, it checks if the checkbox is selected or not
        and changes the current settings with the new value
        """
        # print(f"toggleValue is {toggleValue}")
        if toggle_value:
            settings[which_setting] = 1
        else:
            settings[which_setting] = 0

    def save_settings(self, settings):
        """
        Called when ckicking on Save Settings
        """
        if messagebox.askokcancel("Save Settings", "Do you want to save settings?"):
            config.save_settings(settings)

    def shutdown(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            if self.midi_interface:
                self.midi_interface.close_port()
                del self.midi_interface
            sys.exit()

    def flash(self, which_value):
        """
        Flash the IN/OUT labels when a midi message is received or
        a chamsys out message is sent out
        which_value can be "MIDI", "chamsys" or "ERROR"
        """

        if which_value == "MIDI":
            self.midi_in_label.config(fg="#C01914")
            self.midi_in_label.after(200, lambda: self.midi_in_label.config(fg="white"))

        if which_value == "chamsys":
            self.chamsys_out_label.config(fg="#C01914")
            self.chamsys_out_label.after(
                200, lambda: self.chamsys_out_label.config(fg="white")
            )

        if which_value == "ERROR":
            self.error_label.config(fg="#C01914")
            self.error_label.after(1000, lambda: self.error_label.config(fg="black"))
